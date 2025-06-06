from PIL import Image, ImageDraw
import io


class DrawCube:
    def __init__(self):
        self.face_id = [[0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1]]
        self.color = {
            **dict.fromkeys(range(1, 10), "red"),
            **dict.fromkeys(range(10, 19), "blue"),
            **dict.fromkeys(range(19, 28), "yellow"),
            **dict.fromkeys(range(28, 37), "orange"),
            **dict.fromkeys(range(37, 46), "green"),
            **dict.fromkeys(range(46, 55), "white"),
        }

    def _clear_image(self):
        self.img = Image.new("RGB", (525, 275), color="black")

    def _draw(self, dx, dy, arr):
        drawer = ImageDraw.Draw(self.img)
        dx *= 100
        dy *= 100
        cons = 25
        for conty, row in enumerate(arr):
            for contx, j in enumerate(row):
                posx = contx * cons + dx
                posy = conty * cons + dy
                drawer.rectangle((posx, posy, posx + 20, posy + 20), fill=self.color[j])

    def _draw_all_cube(self, lst):
        for i in range(len(lst)):
            self._draw(self.face_id[i][1], self.face_id[i][0], lst[i])

    def _prjctn(self, lst):
        draw = ImageDraw.Draw(self.img)
        dx, dy, cons = 400, 100, 25
        for conty, row in enumerate(lst[2]):
            for contx, j in enumerate(row):
                posx = contx * cons + dx
                posy = conty * cons + dy
                draw.rectangle((posx, posy, posx + 20, posy + 20), fill=self.color[j])

        dx, dy = 470, 84
        for row in lst[0][::-1]:
            for j in row[::-1]:
                draw.polygon(
                    [
                        (11 + dx, 0 + dy),
                        (-9 + dx, 0 + dy),
                        (-20 + dx, 11 + dy),
                        (0 + dx, 11 + dy),
                    ],
                    fill=self.color[j],
                )
                dx -= 25
            dy -= 14
            dx += 91

        dx, dy = 474, 87
        for row in lst[3]:
            for j in row:
                draw.polygon(
                    [
                        (11 + dx, 0 + dy),
                        (0 + dx, 11 + dy),
                        (0 + dx, 31 + dy),
                        (11 + dx, 20 + dy),
                    ],
                    fill=self.color[j],
                )
                dx += 16
                dy -= 13
            dx = 474
            dy += 64.5

    def draw(self, newmf) -> bytes:
        """
        渲染图像并返回字节内容
        :param newmf: 魔方六面数据列表，格式为 [U, R, F, D, L, B]
        :return: PNG 格式图像字节
        """
        self._clear_image()
        lst = [newmf[4], newmf[2], newmf[0], newmf[3], newmf[1], newmf[5]]  # 按需重排面
        self._draw_all_cube(lst)
        self._prjctn(lst)
        buf = io.BytesIO()
        self.img.save(buf, format="PNG")
        return buf.getvalue()
