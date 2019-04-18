import pygame
from pyscroll import BufferedRenderer


class RogueRenderer(BufferedRenderer):
    def center(self, coords):
        """ center the map on a pixel
        float numbers will be rounded.
        :param coords: (number, number)
        """
        vec = pygame.Vector2(coords[0], coords[1])
        camera = pygame.Vector2(self.view_rect.center)
        new_center = camera + (vec - camera) * 0.02
        self.view_rect.center = (round(new_center.x), round(new_center.y))

        tw, th = self.data.tile_size

        if self.clamp_camera:
            # prevent camera from exposing edges of the map
            self._anchored_view = True
            self.view_rect.clamp_ip(self.map_rect)
            x, y = self.view_rect.center
            left, self._x_offset = divmod(x - self._half_width, tw)
            top, self._y_offset = divmod(y - self._half_height, th)
        else:
            x, y = self.view_rect.center
            # calc the new position in tiles and pixel offset
            left, self._x_offset = divmod(x - self._half_width, tw)
            top, self._y_offset = divmod(y - self._half_height, th)
            mw, mh = self.data.map_size
            vw, vh = self._tile_view.size
            right = left + vw
            bottom = top + vh

            # not anchored, so the rendered map is being offset by values larger
            # than the tile size.  this occurs when the edges of the map are inside
            # the screen.  a situation like is shows a background under the map.
            self._anchored_view = True
            dx = int(left - self._tile_view.left)
            dy = int(top - self._tile_view.top)

            if mw < vw or left < 0:
                left = 0
                self._x_offset = x - self._half_width
                self._anchored_view = False

            elif right > mw:
                left = mw - vw
                self._x_offset += dx * tw
                self._anchored_view = False

            if mh < vh or top < 0:
                top = 0
                self._y_offset = y - self._half_height
                self._anchored_view = False

            elif bottom > mh:
                top = mh - vh
                self._y_offset += dy * th
                self._anchored_view = False

        # adjust the view if the view has changed without a redraw
        dx = int(left - self._tile_view.left)
        dy = int(top - self._tile_view.top)
        view_change = max(abs(dx), abs(dy))

        if view_change and (view_change <= self._redraw_cutoff):
            self._buffer.scroll(-dx * tw, -dy * th)
            self._tile_view.move_ip(dx, dy)
            self._queue_edge_tiles(dx, dy)
            self._flush_tile_queue(self._buffer)

        elif view_change > self._redraw_cutoff:
            print('scrolling too quickly.  redraw forced')
            self._tile_view.move_ip(dx, dy)
            self.redraw_tiles(self._buffer)
