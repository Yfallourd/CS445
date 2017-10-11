import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
try:
    import TableLamp.src.Lightbulb.Lightbulb as lb
    import TableLamp.src.Button.PushButton as pb
except ImportError:
    print("Please make sure you are running main.py from the src folder")
if __name__ == "__main__":
    lightbulb = lb.Lightbulb()
    button = pb.PushButton(lightbulb)

    button.PushButton()
    button.PushButton()

