def get_stderr(capfd):
    def exists(val):
        if val and val != "\n":
            return True

        return False

    output = capfd.readouterr().err.split("\n")
    output = [item.rstrip() for item in output if exists(item)]

    return output
