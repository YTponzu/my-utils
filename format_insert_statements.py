#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLファイルのINSERT文を1レコードずつ改行するスクリプト

【使い方】
1. このスクリプトをSQLファイルと同じディレクトリに配置
2. コマンドラインで以下を実行:
   python format_insert_statements.py

【動作】
- カレントディレクトリ内の全ての.sqlファイルを自動検索
- INSERT INTO `tablename` VALUES (...),(...); 形式の文を検出
- 各レコード (...)ごとに改行して整形
- 結果を 'formatted_sql' フォルダに出力

【変換例】
変換前:
  INSERT INTO `users` VALUES (1,'太郎'),(2,'花子'),(3,'次郎');

変換後:
  INSERT INTO `users` VALUES
  (1,'太郎'),
  (2,'花子'),
  (3,'次郎');

【注意】
- 文字列内のカンマやエスケープ文字も正しく処理されます
- 元のファイルは変更されません（新しいフォルダに出力）
- UTF-8エンコーディングで処理されます
"""
import re
import os
import glob

def format_insert_statements(input_file, output_file):
    """
    INSERT文を1レコードずつ改行して出力する
    
    Args:
        input_file: 入力SQLファイルのパス
        output_file: 出力SQLファイルのパス
    """
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # INSERT INTO文を検索して処理
    # パターン: INSERT INTO `tablename` VALUES (...),(...);
    insert_pattern = r'(INSERT INTO\s+`[^`]+`\s+VALUES\s+)(\([^;]+\);)'
    
    def format_values(match):
        insert_clause = match.group(1)  # INSERT INTO `tablename` VALUES 
        values_clause = match.group(2)  # (...),(...);
        
        # 値の部分を処理（セミコロンを除く）
        values_without_semicolon = values_clause.rstrip(';')
        
        # レコードを分割（括弧の対応を考慮）
        records = []
        current_record = ''
        paren_count = 0
        in_string = False
        escape_next = False
        string_char = None
        
        for i, char in enumerate(values_without_semicolon):
            if escape_next:
                current_record += char
                escape_next = False
                continue
            
            if char == '\\':
                current_record += char
                escape_next = True
                continue
            
            if char in ('"', "'") and not in_string:
                in_string = True
                string_char = char
                current_record += char
            elif char == string_char and in_string:
                in_string = False
                string_char = None
                current_record += char
            elif char == '(' and not in_string:
                paren_count += 1
                current_record += char
            elif char == ')' and not in_string:
                paren_count -= 1
                current_record += char
                if paren_count == 0:
                    # レコードの終わり
                    records.append(current_record.strip())
                    current_record = ''
                    # 次のカンマとスペースをスキップ
                    if i + 1 < len(values_without_semicolon) and values_without_semicolon[i + 1] == ',':
                        continue
            else:
                if paren_count > 0 or char != ',':
                    current_record += char
        
        # 最後のレコードが残っている場合
        if current_record.strip():
            records.append(current_record.strip())
        
        # フォーマット: 各レコードを改行で区切る
        if records:
            formatted = insert_clause + '\n'
            for i, record in enumerate(records):
                if i < len(records) - 1:
                    formatted += record + ',\n'
                else:
                    formatted += record + ';\n'
            return formatted
        else:
            return match.group(0)
    
    # INSERT文をフォーマット
    formatted_content = re.sub(insert_pattern, format_values, content, flags=re.IGNORECASE | re.DOTALL)
    
    # 出力ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_content)
    
    print(f"処理完了: {input_file} -> {output_file}")

def main():
    # カレントディレクトリの全SQLファイルを処理
    sql_files = glob.glob('*.sql')
    
    if not sql_files:
        print("SQLファイルが見つかりません")
        return
    
    # 出力ディレクトリを作成
    output_dir = 'formatted_sql'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"{len(sql_files)}個のSQLファイルを処理します...\n")
    
    for sql_file in sql_files:
        output_file = os.path.join(output_dir, sql_file)
        format_insert_statements(sql_file, output_file)
    
    print(f"\n全ての処理が完了しました。出力ディレクトリ: {output_dir}")

if __name__ == '__main__':
    main()
