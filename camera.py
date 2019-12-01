from PIL import Image, ImageTk
import cv2 

class Camera(cv2.VideoCapture):

    __mirror = False

    def read(self):
        
        """
        Retorna um PhotoImage e o tamanho da imagem.
        """

        # Obtém frame da câmera.
        status , frame = super().read()

        if not status: return

        # Obtém a imagem.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        
        # Se a opção de efeito espelho estiver ativa, a imagem será invertida.
        if self.__mirror:
            frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
        
        return ImageTk.PhotoImage(frame) , frame.size


    def mirror(self):

        """
        Habilita ou desabilita o efeito espelho.
        """
        self.__mirror = not self.__mirror
