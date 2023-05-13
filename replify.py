import json


def test(x=2):
    return "Working Fine" * x


class REPLify:
    def __init__(self, namespace=None):
        self.count = 0
        self.namespace = namespace if namespace else {}

    def process_input(self, input_text):
        try:
            # evaluate the input in the namespace
            input_data = eval(input_text, self.namespace)
            # do some computation here...
            output_data = {"data": input_data, "info": {"count": self.count}}
        except Exception as e:
            # if there was an error, return an error message
            output_data = {"error": str(e)}

        # convert the output to JSON and print it
        output_text = json.dumps(output_data)
        print(output_text)

    def start_listening(self):
        # read input from stdin, process it, and write output to stdout
        while True:
            input_text = input().strip()
            self.count += 1
            if not input_text:
                break
            self.process_input(input_text)


if __name__ == "__main__":
    REPLify().start_listening()
