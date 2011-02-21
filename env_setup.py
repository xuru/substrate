import sys, os


def setup():
    if 'lib' not in sys.path:
        sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

    # from hulk import env
    # if env.on_development_server:
    #     sys.path.append(os.path.join(os.path.dirname(__file__), "local/ext"))

