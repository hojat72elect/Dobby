import numpy

class Triangle:
    def __init__(self, app):
        self.app = app
        self.opengl_context = app.opengl_context

    def get_vertex_data(self):
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
        vertex_data = numpy.array(vertex_data, dtype='f4')
        return vertex_data

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.opengl_context.buffer(vertex_data)
        return vbo