import pygame


class Dialog:
    def __init__(self, file):
        # self.pachi = pygame.image.load("pachie.png").convert_alpha()
        #  self.scarlet = pygame.image.load("scarlete.png").convert_alpha()
        #self.dialogBox = pygame.image.load("diaPane.png").convert_alpha()
        #font1 = pygame.font.SysFont(""arial", 20)
        self.texts = []
        self.Pane = pygame.image.load("diaPane.png").convert_alpha()
        self.pos = (130, 340)
        with open(file, 'r') as f:
            line = f.readline()
            while line:
                self.texts.append(line)
                print("111")
                line = f.readline()
        self.chapter = 1
        print(self.texts)

    def proceedCon(self, chapter, target):
        line = 0
        for i in range(0, len(self.texts)):
            if self.texts[i][:-1] == "chapter" + str(chapter):
                line = i + 1
        for i in range(line, len(self.texts)):
            if self.texts[i] == '\n':
                break
            target.blit()







def main():  #
    a = Dialog("DL.txt")
    a.proceedConver(1,1)



if __name__ == "__main__":
    main()
