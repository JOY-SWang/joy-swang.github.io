# Answer Matcher 使用说明

## 功能简介

`answer_matcher.py` 提供了一个智能的答案匹配函数 `check_answer_match()`，用于判断模型预测的答案（prediction）和标准答案（golden）是否一致。

## 主要特性

1. **多格式支持**：
   - 支持带选项字母的答案：`(c) observing a meteor shower`、`B) project meeting`
   - 支持纯文本答案：`There are five speakers in the conversation.`

2. **智能匹配策略**：
   - 直接选项字母匹配
   - 文本相似度匹配（基于单词级和字符级）
   - 关键词提取和匹配
   - 停用词过滤

3. **灵活的阈值设置**：
   - 默认相似度阈值：0.7
   - 可根据需求调整阈值

## 函数签名

```python
check_answer_match(golden, prediction, question=None, similarity_threshold=0.7)
```

### 参数说明

- `golden` (str): 标准答案字符串，通常包含 `<RESPONSE>` 标签和答案选项
  - 例如: `"<RESPONSE>The answer is C.</RESPONSE>"`
  - 或: `"<RESPONSE>C. There are five speakers...</RESPONSE>"`

- `prediction` (str): 模型预测的答案
  - 单独字母: `"C"`
  - 带选项: `"(c) observing a meteor shower"`、`"B) project meeting"`
  - 不带选项: `"There are five speakers in the conversation."`

- `question` (str, optional): 问题文本，包含选项列表
  - 当 prediction 不包含明确选项字母时**必须提供**
  - 例如: `"What is the context? (a) casual chat (b) project meeting (c) phone call"`

- `similarity_threshold` (float): 文本相似度阈值，默认 0.7
  - 范围: 0.0 - 1.0
  - 建议: 0.5 - 0.8

### 返回值

- `bool`: True 表示答案一致，False 表示不一致

## 使用示例

### 示例 1: prediction 是单独的字母

```python
from answer_matcher import check_answer_match

golden = "<RESPONSE>The answer is C.</RESPONSE>"
prediction = "C"

result = check_answer_match(golden, prediction)
print(result)  # True
```

### 示例 2: prediction 包含选项字母和描述

```python
golden = "<RESPONSE>The answer is C.</RESPONSE>"
prediction = "(c) observing a meteor shower"

result = check_answer_match(golden, prediction)
print(result)  # True
```

### 示例 3: prediction 不包含选项字母

```python
golden = "<RESPONSE>The answer is B.</RESPONSE>"
prediction = "It sounds like a project meeting among colleagues."
question = "What is the context? (a) casual chat (b) project meeting (c) phone call (d) classroom"

result = check_answer_match(golden, prediction, question)
print(result)  # True
```

### 示例 4: 数字答案匹配

```python
golden = "<RESPONSE>C. There are five distinct voices...</RESPONSE>"
prediction = "There are five speakers in the conversation."
question = "How many speakers? (a) three (b) four (c) five (d) six"

result = check_answer_match(golden, prediction, question)
print(result)  # True
```

### 示例 5: 自定义相似度阈值

```python
golden = "<RESPONSE>The answer is A.</RESPONSE>"
prediction = "An informal conversation between friends."
question = "What is the context? (a) casual chat between friends (b) formal meeting"

# 使用较低阈值以允许更宽松的匹配
result = check_answer_match(golden, prediction, question, similarity_threshold=0.5)
print(result)  # True (相似度约 0.52)
```

## 相似度计算策略

函数使用多种策略来计算文本相似度：

1. **单词级包含关系**：如果一个文本的所有单词都在另一个文本中，相似度 = 0.9
   - 例如: "five" 包含在 "There are five speakers"

2. **字符级包含关系**：如果一个文本是另一个的子串，相似度基于长度比例
   - 相似度 = (较短文本长度 / 较长文本长度) + 0.5

3. **关键词匹配**：移除停用词后计算词重叠率
   - 相似度 = 交集单词数 / 并集单词数

4. **序列相似度**：使用 SequenceMatcher 计算字符序列相似度

最终相似度取以上策略的**最大值**。

## 注意事项

1. **必须提供 question 的情况**：
   - 当 prediction 不包含明确的选项字母时，必须提供 question 参数
   - 否则函数会打印警告并返回 False

2. **选项格式要求**：
   - golden 中的答案格式：`"The answer is C."` 或 `"C. Some text..."`
   - prediction 中的选项格式：
     - 单独字母：`"C"`、`"c"`
     - 带括号：`"(c)"`、`"(C)"`
     - 带括号和描述：`"(c) some description"`
     - 字母后跟括号：`"c)"` 、`"C)"`
     - 字母后跟句点：`"C."`、`"c."`
   - question 中的选项格式：`(a) option text`

3. **语义相似性限制**：
   - 当前实现基于词汇匹配，不支持深度语义理解
   - 例如 "informal conversation" 和 "casual chat" 相似度较低（约 0.52）
   - 如需支持语义相似性，建议降低阈值或使用词嵌入技术

4. **阈值选择建议**：
   - 严格匹配：0.7 - 0.8
   - 宽松匹配：0.5 - 0.6
   - 非常宽松：0.3 - 0.4

## 测试

运行内置测试用例：

```bash
python scripts/answer_matcher.py
```

测试覆盖场景：
- 带选项字母的 prediction
- 不带选项字母的 prediction
- 不同选项格式
- 数字答案匹配
- 错误答案识别
- 边界情况测试

## 依赖

- Python 3.6+
- 标准库: `re`, `difflib`

无需安装额外依赖包。

