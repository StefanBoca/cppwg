#!/usr/bin/env python

"""
Parse the single header file using CastXML and pygccxml
"""

import os

from pygccxml import parser, declarations
import castxml


class CppSourceParser:
    def __init__(
        self, source_root, wrapper_header_collection, source_includes
    ):

        self.source_root = source_root
        self.wrapper_header_collection = wrapper_header_collection
        self.source_includes = source_includes
        self.global_ns = None
        self.source_ns = None

    def parse(self):

        xml_generator_config = parser.xml_generator_configuration_t(
            xml_generator_path=os.join(castxml.BIN_DIR, 'castxml'),
            xml_generator="castxml",
            cflags="-std=c++11",
            include_paths=self.source_includes,
        )

        print("INFO: Parsing Code")
        decls = parser.parse(
            [self.wrapper_header_collection],
            xml_generator_config,
            compilation_mode=parser.COMPILATION_MODE.ALL_AT_ONCE,
        )

        # Get access to the global namespace
        self.global_ns = declarations.get_global_namespace(decls)

        # Clean decls to only include those for which file locations exist
        print("INFO: Cleaning Decls")
        query = declarations.custom_matcher_t(lambda decl: decl.location is not None)
        decls_loc_not_none = self.global_ns.decls(function=query)

        # Identify decls in our source tree
        def check_loc(loc):
            return (self.source_root in loc) or ("wrapper_header_collection" in loc)

        source_decls = [
            decl for decl in decls_loc_not_none if check_loc(decl.location.file_name)
        ]
        self.source_ns = declarations.namespace_t("source", source_decls)

        print("INFO: Optimizing Decls")
        self.source_ns.init_optimizer()
