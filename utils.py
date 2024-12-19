import re
import math
import pickle

def _load_model():
    filename = 'model-webshell.pickle'
    model = pickle.load(open(filename, "rb"))
    print("Loaded model")
    return model

# Khai báo các hàm tiền xử lý dữ liệu
def process(input_text):
    # Sử dụng biểu thức chính quy để tìm và thay thế các đoạn comment
    pattern = re.compile(r'/\*.*?\*/', re.DOTALL)
    result = re.sub(pattern, '', input_text)

    lines = result.split("\n")
    # Xoá các dòng trắng
    non_blank_lines = filter(lambda line: line.strip() != "", lines)
    final = "\n".join(non_blank_lines)
    return final

#  Tính entropy information của file
def calculate_entropy(text):
    # Tạo một từ điển đếm tần suất xuất hiện của từng ký tự trong văn bản
    char_count = {}
    total_chars = len(text)

    for char in text:
        char_count[char] = char_count.get(char, 0) + 1

    # Tính toán entropy theo công thức
    entropy = -sum((count/total_chars) * math.log2(count/total_chars) for count in char_count.values())

    return round(entropy,3)
# Đếm số lượng các câu lệnh lặp trong file
def cal_loop_ratio(code):
    total_lines = code.split('\n')

    # Tính tỷ lệ
    if len(total_lines) > 0:
        pattern_for = re.compile(r'for[ ]*\(')
        pattern_foreach = re.compile(r'foreach[ ]*\(')
        pattern_elseif = re.compile(r'elseif')
        ratio = list()
        match_els = list()
        match_for = list()
        match_fore = list()

        match_els = pattern_elseif.findall(code)
        match_for = pattern_for.findall(code)
        match_fore = pattern_foreach.findall(code)

        for i in range(3):
          ratio.append(round((len(match_els) / len(total_lines)), 3))
          ratio.append(round((len(match_for) / len(total_lines)), 3))
          ratio.append(round((len(match_fore) / len(total_lines)), 3))

        return ratio
    else:
        return [0,0,0]
# Đếm số lượng từ xuất hiện trong file
def count_word(file, word_array):
    count_list = list()
    for word in word_array:
      count_list.append(file.count(word))

    return count_list;

def extract_php_code(text):
    pattern = re.compile(r'<\?[php]?(.*?)\?>', re.DOTALL)
    result=""
    matches = pattern.findall(text)
    for code_block in matches:
        result += code_block.strip()

    return result;

# Đếm số lượng các hàm nguy hiểm trong file
def cal_mal_func(code, mal_func_arr):
  temp = extract_php_code(code)
  result = count_word(temp, mal_func_arr)

  return sum(result)
# Đếm số ký tự trên 1 dòng trong file
def count_max_len_line(code):
  total_lines = extract_php_code(code)
  total_lines = total_lines.split('\n')
  max_len = max(total_lines, key=len)

  return len(max_len)
# Tìm từ dài nhất
def count_max_len_word(code):
  words = code.split()
  word_list = filter(filter_url, words)
  max_word = max(word_list, key=len)

  return len(max_word)
def filter_url(input):
  fil_value = 'http://'
  if fil_value in input:
    return False

  return True;