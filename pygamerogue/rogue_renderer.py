from pyscroll import BufferedRenderer


class RogueRenderer(BufferedRenderer):
    def center(self, coords):
        """ center the map on a pixel
        float numbers will be rounded.
        :param coords: (number, number)
        """
        x, y = round(coords[0]), round(coords[1])
        self.view_rect.center = x, y

        tw, th = self.data.tile_size

        # prevent camera from exposing edges of the map
        self._anchored_view = True
        self.view_rect.clamp_ip(self.map_rect)
        x, y = self.view_rect.center

        # calc the new position in tiles and pixel offset
        left, self._x_offset = divmod(x - self._half_width, tw)
        top, self._y_offset = divmod(y - self._half_height, th)

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
