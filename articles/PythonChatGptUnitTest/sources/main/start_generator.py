from test_generator import TestGenerator
import sys

source_file = sys.argv[1]
print(f"Generating test file for {source_file}")

test_file = TestGenerator().create_test_file(source_file)
print(f"Test file generated : {test_file}")
