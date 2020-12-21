class Variable:
  def __init__(self, name):
    self.name = name

  def _formater(self):
    return f'{self.name}'
  
  def __str__(self):
    return self._formater()

  def __repr__(self):
    return self._formater()

  def __hash__(self):
    return f'v-{self.name}'.__hash__()

  def __eq__(self, other):
    if not isinstance(other, Variable):
      return False
    if other.name != self.name:
      return False
    return True

  def __ne__(self, other):
    if not isinstance(other, Variable):
      return True
    if other.name != self.name:
      return True
    return False

class Term:
  def __init__(self, name, args = []):
    self.name = name
    self.args = args

  def _formater(self):
    if self.args:
      return f'{self.name}{self.args}'
    return f'{self.name}'
  
  def __str__(self):
    return self._formater()

  def __repr__(self):
    return self._formater()

  def __hash__(self):
    return f't-{self.name}{self.args}'.__hash__()

  def __eq__(self, other):
    if not isinstance(other, Term):
      return False
    if other.name != self.name:
      return False
    for i in range(len(self.args)):
      if self.args[i] != other.args[i]:
        return False
    return True

  def __ne__(self, other):
    if not isinstance(other, Term):
      return True
    if other.name != self.name:
      return True
    for i in range(len(self.args)):
      if self.args[i] != other.args[i]:
        return True
    return False

  def match(self, other):
    # assert(isinstance(other, Term))
    if other.name == self.name and len(other.args) == len(self.args):
      return True
    return False

  def compareArgs(self, other):
    # assert(isinstance(other, Term))
    for i in range(len(self.args)):
      if not isinstance(other.args[i], Term) or\
        not isinstance(self.args[i], Term):
        continue
      if other.args[i].name != self.args[i].name:
        return False
    return True

  def getBindings(self, other):
    """
      Get the terms into other.args that is at the
    same position of the variables into self.args 
    and associate (variables -> terms) into a dict. 
    """
    # assert(isinstance(other, Term))
    bindings = {}
    for i in range(len(self.args)):
      if isinstance(self.args[i], Variable):
        bindings[self.args[i]] = other.args[i]
    return bindings

  def substituteByBindings(self, bindings):
    """
      Receive a map with the name of the variables
    of self.args that must be change by the new values.
    Return a complete new Term object.
    """
    newArgs = []
    for arg in self.args:
      changed = False
      for (key, value) in bindings.items():
        if key.name == arg.name:
          newArgs.append(value)
          changed = True
          break
      if not changed:
        newArgs.append(arg)

    return Term(self.name, newArgs)

  def substitute(self, other):
    """
      Substitute the variables int self.args by the
    terms into other.args at the same index of each
    variables into self.args.
    Return a complete new Term object.
    """
    # assert(isinstance(other, Term))
    if not self.match(other):
      return None
    newArgs = []
    for i in range(len(self.args)):
      if isinstance(self.args[i], Variable):
        newArgs.append(other.args[i])
      else:
        newArgs.append(self.args[i])
    return Term(self.name, newArgs)

class TRUE:
  def __init__(self):
    self.name = 'true'

class Rule:
  def __init__(self, consequence, conditional):
    self.consequence = consequence
    self.conditional = conditional

class Database:
  def __init__(self):
    self.facts = []
    self.rules = []

  def addRule(self, rule):
    self.rules.append(rule)

  def addFact(self, fact):
    self.facts.append(fact)

  def query(self, goal):
    retuned_answers = set()
    for rule in self.rules:
      if goal.match(rule.consequence):
        bindings = rule.consequence.getBindings(goal)
        consequence = rule.consequence.substituteByBindings(bindings)
        conditional = rule.conditional.substituteByBindings(bindings)
        for fact in self.facts:
          if conditional.match(fact) and conditional.compareArgs(fact):
            bindings = conditional.getBindings(fact)
            answer = consequence.substituteByBindings(bindings)
            if answer not in retuned_answers:
              retuned_answers.add(answer)
              yield answer
    for fact in self.facts:
      if goal.match(fact) and goal.compareArgs(fact):
        bindings = goal.getBindings(fact)
        answer = goal.substituteByBindings(bindings)
        if answer not in retuned_answers:
          retuned_answers.add(answer)
          yield answer

if __name__ == '__main__':
  # know = Term('dad', [ Term('Patro'), Term('Nalbert') ])
  # goal = Term('dad', [ Term('Patro'), Variable('X') ])
  # bindings = goal.getBindings(know)
  # term = goal.substituteByBindings(bindings)

  db = Database()
  db.addFact( Term('dad', [ Term('Patro'), Term('Nalbert') ]))
  db.addFact( Term('dad', [ Term('Patro'), Term('Herbert') ]))
  db.addFact( Term('child', [ Term('Nalbert'), Term('Patro') ]))
  db.addFact( Term('child', [ Term('Herbert'), Term('Patro') ]))
  db.addFact( Term('brothers', [ Term('Herbert'), Term('Nalbert') ]))
  db.addFact( Term('brothers', [ Term('Nalbert'), Term('Herbert') ]))
  # db.addFact( Term('brothers', [ Term('Nalbert'),Term('Herbert') ]))

  rule1 = Rule(
    Term('dad', [ Variable('X'), Variable('Y')]),
    Term('child', [ Variable('Y'), Variable('X')])
  )

  # rule1 = Rule(
  #   Term('brothers', [ Variable('X'), Variable('Y')]),
  #   Conjunction([
  #     Term('dad', [ Variable('Z'), Variable('X')]),
  #     Term('dad', [ Variable('Z'), Variable('Y')])
  #   ])
  # )

  db.addRule(rule1)

  term = db.query( Term('dad', [ Term('Patro'), Variable('K') ] ) )
  print(next(term))
  print(next(term))

  term = db.query( Term('brothers', [ Term('Herbert'), Variable('X') ] ) )
  print(next(term))