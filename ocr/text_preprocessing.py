import re

class TextProcessor:
    def __init__(self):
        self.pattern = r'\(.*?[\)\]\}>\)]|\[.*?[\)\]\}>\)]|\{.*?[\)\]\}>\)]|\<.*?[\)\]\}>\)]'

    def preprocess_text(self, text):
        modified_text = re.sub(self.pattern, '', text)
        modified_text = modified_text.strip()
        return modified_text

    def process_ocr(self, ocr):
        ocr_list = []
        for item in ocr:
            modified_item = self.preprocess_text(item)
            if modified_item != '':
                ocr_list.append(modified_item)

        ocr = [x.split('(')[0] if '(' in x else x for x in ocr_list]
        ocr = [x.split('[')[0] if '[' in x else x for x in ocr]
        ocr = [g.replace('MG', 'mg') for g in ocr]
        ocr = [g.replace('캅', '캡') for g in ocr]
        ocr = [g.replace('비)', '') for g in ocr]
        ocr = [g.replace('본)', '') for g in ocr]
        ocr = [g.replace('경구', '') for g in ocr]
        ocr = [g.replace(' ', '') for g in ocr]
        ocr = [g.replace('mgT', '') for g in ocr]
        ocr = [g.replace('mgIT', '') for g in ocr]
        ocr = [g.replace('mg/T', '') for g in ocr]
        ocr = [g.replace('mgI', '') for g in ocr]
        ocr = [g.replace('mg/C', '') for g in ocr]
        ocr = [g.replace('mgC', '') for g in ocr]
        ocr = [g.replace('101120C', '') for g in ocr]
        ocr = [g.replace('1일', '') for g in ocr]
        ocr = [g.replace('"', '') for g in ocr]
        ocr = [g.replace("'", '') for g in ocr]
        ocr = [g.replace('`', '') for g in ocr]
        ocr = [g.replace('!', '') for g in ocr]
        ocr = [g.replace('@', '') for g in ocr]
        ocr = [g.replace('#', '') for g in ocr]
        ocr = [g.replace('$', '') for g in ocr]
        ocr = [g.replace('^', '') for g in ocr]
        ocr = [g.replace('&', '') for g in ocr]
        ocr = [g.replace('*', '') for g in ocr]
        ocr = [g.replace('-', '') for g in ocr]
        ocr = [g.replace('_', '') for g in ocr]
        ocr = [g.replace('=', '') for g in ocr]
        ocr = [g.replace('+', '') for g in ocr]
        ocr = [g.replace(';', '') for g in ocr]
        ocr = [g.replace(':', '') for g in ocr]
        ocr = [g.replace('"', '') for g in ocr]
        ocr = [g.replace("'", '') for g in ocr]
        ocr = [g.replace(',', '') for g in ocr]
        ocr = [g.replace('(', '') for g in ocr]
        ocr = [g.replace('<', '') for g in ocr]
        ocr = [g.replace('<', '') for g in ocr]
        ocr = [g.replace('>', '') for g in ocr]
        return ocr
