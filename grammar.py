from __future__ import print_function
from __future__ import absolute_import

import os
import json

from dom import *

# BASE_DIR_NAME = os.path.dirname(__file__)
DSL_MAPPING_FILEPATH = "dsl-mapping.json"


class Grammar:
    def __init__(self):
        style_json = DSL_MAPPING_FILEPATH
        with open(style_json) as data_file:
            self.dsl_mapping = json.load(data_file)

        self.opening_tag = self.dsl_mapping["opening-tag"]
        self.closing_tag = self.dsl_mapping["closing-tag"]
        self.content_holder = self.opening_tag + self.closing_tag

        self.root = Dom("body", None, self.content_holder)

    def compile(self, generated_gui):
        dsl_file = generated_gui

        #Parse fix
        dsl_file = dsl_file[1:-1]
        dsl_file = ' '.join(dsl_file)
        dsl_file = dsl_file.replace('{', '{8').replace('}', '8}8')
        dsl_file = dsl_file.replace(' ', '')
        dsl_file = dsl_file.split('8')
        dsl_file = list(filter(None, dsl_file))

        current_parent = self.root
        for token in dsl_file:
            token = token.replace(" ", "").replace("\n", "")

            if token.find(self.opening_tag) != -1:
                token = token.replace(self.opening_tag, "")
                element = Dom(token, current_parent, self.content_holder)
                current_parent.add_child(element)
                current_parent = element
            elif token.find(self.closing_tag) != -1:
                current_parent = current_parent.parent
            else:
                tokens = token.split(",")
                for t in tokens:
                    element = Dom(t, current_parent, self.content_holder)
                    current_parent.add_child(element)

        output_html = self.root.render(self.dsl_mapping)
        if output_html is None: return "HTML Parsing Error"

        return output_html