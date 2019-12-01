from camera import *
from config import config
from tkinter import *
from util import *


class App(object):

    line_color = "red"
    line_width = 2

    margin = [50,50]
    mirror_effect = True

    text_color = "red"
    text_font = ("Comic Sans MS",25)

    w_color = "gray2"
    w_title = "Angle Gauge"

    w_width = 640
    w_height = 480

    wm_attributes = (["-transparent","gray2"],)

    event_PAUSE = "<Button-1>"


    def __init__(self,camera = False):

        # Cria janela e a configura adequadamente.
        self.__root = Tk()
        self.__root["bg"] = self.w_color
        self.__root.title(self.w_title)
        self.__root.geometry("{}x{}".format(self.w_width,self.w_height))

        for attr in self.wm_attributes:
            self.__root.wm_attributes(*attr)


        # Cria canvas.
        self.__canvas = Canvas(
            self.__root,
            width = self.w_width,
            height = self.w_height,
            bg = self.w_color,
            highlightthickness = 0
            )
        self.__canvas.pack()

        self.__draw = True
        self.__close = False


        # Se a opção de câmera estiver ativa, a webcam do usuário será inicializada.
        if camera:
            self.__enableCamera = True
            self.__webcam = Camera(0)

            # Verifica se a opção de efeito espelho está ativa.
            if self.mirror_effect:
                self.__webcam.mirror()

            self.__root.resizable(False,False)

        else:
            self.__enableCamera = False
            self.__webcam = None


        # Configura evento para redimensionar a janela.
        self.__root.bind("<Configure>",self.__resize)

        # Configura evento para o programa parar de desenhar.
        if not type(self.event_PAUSE) is str:
            for key in self.event_PAUSE:
                self.__root.bind(key,self.draw)
        else:
            self.__root.bind(self.event_PAUSE,self.draw)

        # Configura evento para aumentar ou diminuir o tamanho da janela.
        if not camera:
            self.__root.bind("<Key-->",lambda event:self.__resize(event,increase=[-10,-10]))
            self.__root.bind("<Key-=>",lambda event:self.__resize(event,increase=[10,10]))

        # Configura evento para sair do programa.
        self.__root.bind("<Escape>",self.close)
        self.__root.protocol("WM_DELETE_WINDOW",self.close)


    def __calculate(self):

        """ 
        Calcula o ângulo.
        """

        # Obtém a posição da base e da linha desenhada pelo usuário.
        b_pos = self.__canvas.bbox("base")
        l_pos = self.__canvas.bbox("line")

        # Obtém a hipotenusa e os catetos.
        c = b_pos[1] - l_pos[1] 
        b = b_pos[2] - self.line_width * 2 - 1 - l_pos[0] 
        a = getHypotenuse(b,c)

        # Obtém o cosseno e o ângulo.  
        # Fórmula: cosseno = cateto adjacente / hipotenusa.
        cos = b / a
        angle = cos2degrees(cos)
        return angle


    def __camera(self,event=None):

        """
        Coloca imagem da câmera do usuário na tela.
        """

        # Verifica se a camera está pronta para ser usada.
        if not self.__webcam or not self.__webcam.isOpened():
            self.__webcam = Camera(0)

        # Obtém o frame e o tamanho do mesmo.
        image = self.__webcam.read()
        size = image[1]
        self.__canvas.imageFromCamera = image[0]

        # Configura a janela para que fique no mesmo tamanho da imagem da webcam.
        if self.w_width != size[0] and self.w_height != size[1]:
            self.__root.geometry("{}x{}".format(*size))

        # Cria a imagem e a deixa no fundo de todos os outros objetos do canvas.
        self.__canvas.delete("camera")
        self.__canvas.create_image(
            self.w_width//2,
            self.w_height//2,
            image = self.__canvas.imageFromCamera, 
            tag = "camera"
            )
        self.__canvas.tag_lower("camera")


    def close(self,event=None):

        """
        Método para fechar o programa.
        """
        self.__close = True


    def draw(self,event=None):

        """
        Habilita ou desabilita função para o usuário desenhar.
        """ 
        self.__draw = not self.__draw


    def __drawAngle(self):

        """
        Informa o ângulo.
        """

        angle = int(self.__calculate() + 0.2)  # Aproxima o resultado.
        
        self.__canvas.delete("angle")
        
        # Cria uma borda.
        self.__canvas.create_rectangle(
            self.margin[0] - 40,
            self.margin[1] // 2 - 20,
            self.margin[0] + 40,
            self.margin[1] // 2 + 20,
            fill = "black", tag = "angle" , outline= self.text_color
            )

        # Cria um texto para inserir o ângulo.
        self.__canvas.create_text(
            self.margin[0],self.margin[1]//2,
            text = str(angle)+"º",
            font = self.text_font,
            fill = self.text_color,
            tag = "angle"
            )


    def __drawBase(self):

        """
        Desenha a base do triângulo.
        """

        self.__canvas.delete("base")
        self.__canvas.create_line(
            self.margin[0], self.w_height - self.margin[1], 
            self.w_width - self.margin[0], self.w_height - self.margin[1],
            width = self.line_width, fill = self.line_color, tag = "base"
            )


    def __drawLine(self,x=None,y=None):

        """
        Método para desenhar a hipotenusa do triângulo com base
        na posição do cursor do mouse do usuário.
        """


        def draw(x1,y1,x2,y2):

            """
            Função para desenhar a linha da hipotenusa.
            """

            self.__canvas.create_line(
                x1 - self.line_width - 1, y1 - self.line_width - 1, x2, y2, 
                width = self.line_width, fill = self.line_color , tag = "line"
                )


        # Obtém a posição da base.
        b_pos = self.__canvas.bbox("base")
        base_x , base_y = b_pos[2:]

        self.__canvas.delete("line")

        # Caso já exista uma posição X,Y não será necessário obter a 
        # posição do mouse do usuário e realizar uma série de verificações.
        if x and y:
            draw(base_x,base_y,x,y)
            return        

        # Obtém a posição X e Y do mouse.
        mouse_x = self.__root.winfo_pointerx() - self.__root.winfo_rootx()
        mouse_y = self.__root.winfo_pointery() - self.__root.winfo_rooty()

        # Verifica se a linha ultrapassou os limites.
        if mouse_y >= b_pos[1]: 
            mouse_y = b_pos[1] + self.line_width

        if mouse_y <= self.margin[1]:
            mouse_y = self.line_width + self.margin[1]

        if mouse_x >= self.w_width - self.margin[0]:
            mouse_x = self.w_width - self.margin[0]

        if mouse_x <= self.margin[0]:
            mouse_x = self.line_width + self.margin[0]


        # Desenha a hipotenusa.
        draw(base_x, base_y, mouse_x, mouse_y)

        self.__mouse_x = mouse_x
        self.__mouse_y = mouse_y
        

    def __resize(self,event=None,increase=None):

        """
        Método para redimensionar a tela.
        """

        if not increase:
            self.w_width = self.__root.winfo_width()
            self.w_height = self.__root.winfo_height()
            
        elif increase and self.w_width + increase[0] >= 300 and self.w_height + increase[1] >= 300:
            self.w_width += increase[0]
            self.w_height += increase[1]
            self.__root.geometry("{}x{}".format(self.w_width,self.w_height))
            
        self.__canvas.config(width=self.w_width,height=self.w_height)
        self.__drawAngle()


    def run(self):

        """
        Inicializa o programa.
        """

        self.__draw = True
        self.__update()
        self.__root.mainloop()


    def __update(self):

        """
        Método para atualizar o programa, realizando animações e outros.
        """

        # Verifica se a opção de câmera está habilitada.
        if self.__enableCamera:
            self.__camera()

        self.__drawBase()

        # Verifica se a opção de desenhar está habilitada.
        if self.__draw:
            self.__drawLine()
            self.__drawAngle()
        else:
            self.__drawLine(self.__mouse_x,self.__mouse_y)

        # Verifica se o usuário pediu para sair.
        # Se sim a janela é fechada e se não, o programa é atualizado.
        if not self.__close:
            self.__root.after(10,self.__update)

        else:
            self.__root.destroy()

            # Caso a câmera do usuário esteja sendo usada, ela será desligada.
            if self.__webcam and self.__webcam.isOpened():
                self.__webcam.release()




if __name__ == '__main__':

    App.event_PAUSE = config["pause_event"]
    App.line_color = config["color"]
    App.line_width = config["line_width"]
    App.mirror_effect = config["mirror_effect"]
    App.text_color = config["color"]

    App.w_color = config["background"]

    if config["transparent"]:
        App.wm_attributes = (["-transparent",config["background"]],)
    else:
        App.wm_attributes = ()


    App(config["camera"]).run()
