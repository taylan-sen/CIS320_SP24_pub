from collections import defaultdict
import socket
#import IPython

class QuizGameServer():
  def __init__(self):
    self.player_quest_answer = {} 
    self.player_score = {} # d[player] =score
    self.quest_answer = {} # d[quest#] = answer
    self.sock = socket.socket(type=socket.SOCK_DGRAM)
    self.sock.bind(('0.0.0.0', 12001))
    print('Bound to 0.0.0.0:12001')

  def calcPlayerScore(self):
    """ Recalculates player_score 
    . resets every player to 0
    . for each player_quest_answer, if correct, increases player score """
    self.player_score = defaultdict(int)
    for player, quest_answer in self.player_quest_answer.items():
      if self.quest_answer[quest_answer[0]] == quest_answer[1]:
        self.player_score[player] += 1
    
  def handlePacket(self, msg, addr):
    """ validates packet, sends response to sender, records answers """
    print('..handlePacket')
    msg_list = msg.decode().split(',')
    if len(msg_list) != 3:
      self.sock.sendto('Invalid message'.encode(),addr)
      return
    self.sock.sendto('answer recorded'.encode(),addr)
    player, quest, answer = msg_list
    if player == 'oracle':
      self.quest_answer[quest] = answer
      self.calcPlayerScore()
      self.writeHtml()
    else:
      self.player_quest_answer[player] = (quest,answer)
 
  def writeHtml(self):
    """ """
    print('writing html')
    filename = 'score.html'
    s = '<!doctype=html>'
    s += '<html><title>Purple Poll Page</title><body>'
    s += '<div><h1>SCORES</h1>'
    s += '<hr>'
    for player in self.player_score:
      s += player + ':' + str(self.player_score[player]) + '<br>'

    s += '</div></body></html>'
    with open(filename,'w') as f:
      f.write(s) 
    print('file written')

  def loop(self):
    while True:
      msg, addr = self.sock.recvfrom(2048)
      self.handlePacket(msg, addr)

myQuiz = QuizGameServer()
myQuiz.loop()
myQuiz.sock.close()
