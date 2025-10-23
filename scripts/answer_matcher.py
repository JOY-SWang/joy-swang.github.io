import re
from difflib import SequenceMatcher


def extract_golden_choice(golden):
    """
    从 golden 中提取答案选项字母
    例如: "The answer is C." -> "C"
          "C. There are five..." -> "C"
    """
    # 匹配 "The answer is X" 或 "answer is X" 模式
    match = re.search(r'[Tt]he answer is ([A-Da-d])[.\s]', golden)
    if match:
        return match.group(1).upper()
    
    # 匹配句首的 "X. " 格式（如 "C. There are five..."）
    match = re.search(r'^([A-Da-d])\.\s+', golden.strip())
    if match:
        return match.group(1).upper()
    
    # 匹配在 RESPONSE 标签后的 "X. " 格式
    match = re.search(r'<RESPONSE>\s*([A-Da-d])\.\s+', golden)
    if match:
        return match.group(1).upper()
    
    # 匹配换行后的 "X. " 格式
    match = re.search(r'\n([A-Da-d])\.\s+', golden)
    if match:
        return match.group(1).upper()
    
    # 匹配其他可能的模式，如直接以选项字母结尾
    match = re.search(r'\b([A-Da-d])\.\s*$', golden)
    if match:
        return match.group(1).upper()
    
    return None


def extract_prediction_choice(prediction):
    """
    从 prediction 中提取答案选项字母
    例如: "(c) observing a meteor shower" -> "C"
          "C" -> "C"
          "B) project meeting" -> "B"
    """
    prediction = prediction.strip()
    
    # 匹配 (x) 格式
    match = re.match(r'^\(([A-Da-d])\)', prediction)
    if match:
        return match.group(1).upper()
    
    # 匹配 x) 格式
    match = re.match(r'^([A-Da-d])\)', prediction)
    if match:
        return match.group(1).upper()
    
    # 匹配单独的字母后跟空格、冒号或句点
    match = re.match(r'^([A-Da-d])[\s:.]', prediction)
    if match:
        return match.group(1).upper()
    
    # 匹配单独的字母（整个字符串就是一个字母）
    match = re.match(r'^([A-Da-d])$', prediction)
    if match:
        return match.group(1).upper()
    
    return None


def parse_question_options(question):
    """
    从问题中解析出所有选项
    返回: dict {选项字母: 选项内容}
    例如: {"A": "a casual chat between friends", "B": "a project meeting among colleagues", ...}
    """
    options = {}
    
    # 匹配 (x) 格式的选项
    pattern = r'\(([a-dA-D])\)\s*([^(]+?)(?=\s*\([a-dA-D]\)|$)'
    matches = re.findall(pattern, question)
    
    for letter, content in matches:
        options[letter.upper()] = content.strip()
    
    return options


def calculate_similarity(text1, text2):
    """
    计算两个文本的相似度 (0-1)
    使用多种策略来处理不同长度的文本
    """
    # 规范化文本：转小写，去除多余空格和标点
    def normalize(text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    norm_text1 = normalize(text1)
    norm_text2 = normalize(text2)
    
    # 将文本分词
    words1 = set(norm_text1.split())
    words2 = set(norm_text2.split())
    
    # 策略1: 检查单词级别的包含关系
    # 如果一个文本的所有单词都在另一个文本中，返回高相似度
    if words1 and words2:
        if words1.issubset(words2) or words2.issubset(words1):
            # 如果所有单词都匹配，返回较高分数
            return 0.9
    
    # 策略1b: 如果一个文本是另一个的子串（字符级包含）
    if norm_text1 in norm_text2 or norm_text2 in norm_text1:
        # 计算较短文本占较长文本的比例，并给予高权重
        shorter = min(len(norm_text1), len(norm_text2))
        longer = max(len(norm_text1), len(norm_text2))
        return min(1.0, shorter / longer + 0.5)  # 加权以提高包含关系的得分
    
    # 策略2: 提取关键词并比较
    
    # 移除常见停用词
    stopwords = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'of', 
                 'for', 'with', 'by', 'from', 'and', 'or', 'but', 'it', 'this', 'that'}
    words1 = words1 - stopwords
    words2 = words2 - stopwords
    
    # 如果没有关键词，使用原词集
    if not words1:
        words1 = set(norm_text1.split())
    if not words2:
        words2 = set(norm_text2.split())
    
    # 计算词重叠率
    if words1 or words2:
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        word_similarity = intersection / union if union > 0 else 0
    else:
        word_similarity = 0
    
    # 策略3: 使用 SequenceMatcher 计算序列相似度
    sequence_similarity = SequenceMatcher(None, norm_text1, norm_text2).ratio()
    
    # 综合三种策略，取最大值
    return max(word_similarity, sequence_similarity)


def check_answer_match(golden, prediction, question=None, similarity_threshold=0.7):
    """
    判断 prediction 和 golden 的答案是否一致
    
    参数:
        golden (str): 包含标准答案的字符串，格式如 "<RESPONSE>...The answer is C.</RESPONSE>"
        prediction (str): 预测的答案，可能包含选项字母或纯文本
        question (str, optional): 问题文本，包含选项列表，用于解析无选项的 prediction
        similarity_threshold (float): 文本相似度阈值，默认 0.7
    
    返回:
        bool: True 表示答案一致，False 表示不一致
    
    示例:
        >>> golden1 = "<RESPONSE>...The answer is C.</RESPONSE>"
        >>> prediction1 = "(c) observing a meteor shower"
        >>> check_answer_match(golden1, prediction1)
        True
        
        >>> golden2 = "<RESPONSE>...The answer is B.</RESPONSE>"
        >>> prediction2 = "It sounds like a project meeting among colleagues."
        >>> question2 = "What is the likely context? (a) casual chat (b) project meeting (c) phone call"
        >>> check_answer_match(golden2, prediction2, question2)
        True
    """
    # 1. 从 golden 中提取答案选项字母
    golden_choice = extract_golden_choice(golden)
    if not golden_choice:
        # 如果无法提取选项，返回 False
        print(f"Warning: Could not extract choice from golden: {golden}")
        return False
    
    # 2. 尝试从 prediction 中提取选项字母
    prediction_choice = extract_prediction_choice(prediction)
    
    # 3. 如果 prediction 包含明确的选项字母，直接比较
    if prediction_choice:
        return prediction_choice == golden_choice
    
    # 4. 如果 prediction 不包含选项字母，需要通过文本相似度匹配
    if question is None:
        print("Warning: question is required when prediction has no explicit choice")
        return False
    
    # 5. 从 question 中解析所有选项
    options = parse_question_options(question)
    
    if not options:
        print(f"Warning: Could not parse options from question: {question}")
        return False
    
    # 6. 根据 golden_choice 找到正确答案文本
    golden_answer_text = options.get(golden_choice)
    
    if not golden_answer_text:
        print(f"Warning: Could not find option {golden_choice} in parsed options")
        return False
    
    # 7. 计算 prediction 和 golden_answer_text 的相似度
    similarity = calculate_similarity(prediction, golden_answer_text)
    
    # 8. 如果相似度超过阈值，认为答案一致
    return similarity >= similarity_threshold


# 测试代码
if __name__ == "__main__":
    # 测试用例 1: prediction 包含选项字母
    golden1 = "<RESPONSE>\nBased on the dialogue, especially the mentions of \"celestial wonder,\" a \"tripod,\" and asking about \"meteors,\" the speakers are likely observing a meteor shower together. The answer is C.\n</RESPONSE>"
    prediction1 = "(c) observing a meteor shower"
    result1 = check_answer_match(golden1, prediction1)
    print(f"Test 1: {result1}")  # 应该输出 True
    
    # 测试用例 2: prediction 不包含选项字母，需要通过相似度匹配
    golden2 = "<RESPONSE>\nThe discussion about marketing strategy, target demographics, and campaign results points towards a professional environment. Therefore, the most likely context is a project meeting among colleagues. The answer is B.\n</RESPONSE>"
    prediction2 = "It sounds like a project meeting among colleagues."
    question2 = "<audio>What is the likely context of the conversation? (a) a casual chat between friends (b) a project meeting among colleagues (c) a phone call between family members (d) a lecture in a classroom"
    result2 = check_answer_match(golden2, prediction2, question2)
    print(f"Test 2: {result2}")  # 应该输出 True
    
    # 测试用例 3: 错误的答案
    golden3 = "<RESPONSE>\nThe answer is A.\n</RESPONSE>"
    prediction3 = "(b) wrong answer"
    result3 = check_answer_match(golden3, prediction3)
    print(f"Test 3: {result3}")  # 应该输出 False
    
    # 测试用例 4: 数字答案
    golden4 = "<RESPONSE>\nC. There are five distinct voices with different opinions and questions, indicating five speakers.\n</RESPONSE>"
    prediction4 = "There are five speakers in the conversation."
    question4 = "<audio>How many speakers are in the conversation? (a) three (b) four (c) five (d) six"
    result4 = check_answer_match(golden4, prediction4, question4)
    print(f"Test 4: {result4}")  # 应该输出 True
    
    # 额外测试：显示相似度
    print("\n--- Similarity Details ---")
    options4 = parse_question_options(question4)
    print(f"Parsed options: {options4}")
    golden_choice4 = extract_golden_choice(golden4)
    print(f"Golden choice: {golden_choice4}")
    golden_text4 = options4.get(golden_choice4)
    print(f"Golden answer text: {golden_text4}")
    similarity4 = calculate_similarity(prediction4, golden_text4)
    print(f"Similarity: {similarity4}")
    
    # 测试用例 5: 另一种格式的 prediction（包含选项但格式不同）
    golden5 = "<RESPONSE>\nThe answer is B.\n</RESPONSE>"
    prediction5 = "B) project meeting"
    result5 = check_answer_match(golden5, prediction5)
    print(f"\nTest 5: {result5}")  # 应该输出 True
    
    # 测试用例 9: prediction 只是单独的字母
    golden9 = "<RESPONSE>\nThe answer is A.\n</RESPONSE>"
    prediction9 = "A"
    result9 = check_answer_match(golden9, prediction9)
    print(f"Test 9 (single letter): {result9}")  # 应该输出 True
    
    # 测试用例 6: 相似的文本（包含关键词）
    golden6 = "The conversation revolves around stars and constellations, indicating they are observing the night sky. Therefore, based on their conversation, the three individuals are likely engaged in stargazing outdoors. The answer is C."
    prediction6 = "C"
    question6 = "What is the context? (a) a casual chat between friends (b) a formal meeting (c) a classroom discussion (d) a phone interview"
    result6 = check_answer_match(golden6, prediction6)
    print(f"Test 6: {result6}")  # 应该输出 True（包含所有关键词）
    
    # 测试用例 8: 边界情况 - 语义相似但词汇不同（可能失败）
    golden8 = "<RESPONSE>\nThe answer is A.\n</RESPONSE>"
    prediction8 = "The speakers are having an informal conversation between friends."
    question8 = "What is the context? (a) a casual chat between friends (b) a formal meeting (c) a classroom discussion (d) a phone interview"
    result8 = check_answer_match(golden8, prediction8, question8, similarity_threshold=0.5)  # 降低阈值
    print(f"Test 8 (lower threshold): {result8}")  # 使用较低阈值应该通过
    
    # 测试用例 7: 完全不匹配
    golden7 = "<RESPONSE>\nThe answer is C.\n</RESPONSE>"
    prediction7 = "The answer is A"
    result7 = check_answer_match(golden7, prediction7)
    print(f"Test 7: {result7}")  # 应该输出 False

