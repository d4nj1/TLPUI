class TlpConfig:
    def __init__(self, raw, linenumber, state, name, value, quote):
        self.raw = raw
        self.linenumber = linenumber
        self.state = state
        self.name = name
        self.value = value
        self.quote = quote
        self.newvalue = None
        self.newstate = None

    def get_raw(self):
        return self.raw

    def get_linenumber(self):
        return self.linenumber

    def get_state(self):
        return self.state

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_quote(self):
        return self.quote

    def get_new_value(self):
        return self.newvalue

    def set_new_value(self, newvalue):
        if newvalue != self.value:
            self.newvalue = newvalue
        else:
            self.newvalue = None

    def get_new_state(self):
        return self.newstate

    def set_new_state(self, newstate):
        if newstate != self.state:
            self.newstate = newstate
        else:
            self.newstate = None


def get_changed_properties(tlpconfig) -> list:
    changedproperties = list()

    for configid in tlpconfig:
        config = tlpconfig[configid]
        newstate = config.get_new_state()
        newvalue = config.get_new_value()

        if newstate == None and newvalue == None:
            continue

        newconfigvalue = ''

        if newstate != None:
            if newstate == False:
                newconfigvalue = '#'
        else:
            if config.get_state() == False:
                newconfigvalue = '#'

        newconfigvalue = newconfigvalue + config.get_name() + '='

        if newvalue != None:
            value = config.get_new_value()
        else:
            value = config.get_value()

        if config.get_quote():
            value = '\"' + value + '\"'

        newconfigvalue += value
        changedproperties.append([config.get_raw(), config.get_linenumber(), newconfigvalue])

    return changedproperties