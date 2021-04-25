from logging import debug
from flask import Flask, render_template, request
import sys

import dymoprint

app = Flask(__name__)

@app.route('/')
def input_page():
    text = request.args.get('text')

    if text != None:
        emulated_args = [text]
        args = dymoprint.parse_args(emulated_args)
        try:
            dymoprint.main(args)
            return render_template('index.html', success="Printed label")
        except dymoprint.DymoPrintException as e:
            # Exceptions already caught by dymoprint
            return render_template('index.html', error=e.message)
        except Exception:    
            # All other generic errors that might happen
            if not args.pdb:
                raise
            import traceback
            import pdb
            type, value, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem(tb)

    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', debug=False)