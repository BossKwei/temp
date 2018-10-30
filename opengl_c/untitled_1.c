#include <stdio.h>
#include <stdlib.h>

// Do not include the OpenGL header yourself, as
// GLFW does this for you in a platform-independent way.
// If you do need to include such headers, include
// them before the GLFW header and it will detect this.
#include "glad/glad.h"
#include <GLFW/glfw3.h>

// mat4x4 operation
#include "linmath.h"


typedef struct {
    float x, y;
    float r, g, b;
} VERTEX;


static VERTEX vertices[3] = {
        {-0.6f, -0.4f, 1.0f, 0.0f, 0.0f},
        {0.6f,  -0.4f, 0.0f, 1.0f, 0.0f},
        {0.0f,  0.6f,  0.0f, 0.0f, 1.0f}
};


static const char *vertex_shader_text =
        "uniform mat4 MVP;\n"  // per-primitive, constant during an entire draw call
        "attribute vec3 vColor;\n"  // per-vertex, positions, normals, colors, UVs
        "attribute vec2 vPosition;\n"
        "varying vec3 color;\n"  // per-fragment
        "void main()\n"
        "{\n"
        "    gl_Position = MVP * vec4(vPosition, 0.0, 1.0);\n"
        "    color = vColor;\n"
        "}\n";

static const char *fragment_shader_text =
        "varying vec3 color;\n"
        "void main()\n"
        "{\n"
        "    gl_FragColor = vec4(color, 1.0);\n"
        "}\n";


void error_callback(int error, const char *description) {
    fprintf(stderr, "Error: %d %s\n", error, description);
}


void key_callback(GLFWwindow *window, int key, int code, int action, int mods) {
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        glfwSetWindowShouldClose(window, GLFW_TRUE);
}


void reshape_callback(GLFWwindow *window, int width, int height) {
}


GLuint create_shader(GLenum type, const char *text) {
    GLuint shader;
    shader = glCreateShader(type);
    glShaderSource(shader, 1, &text, NULL);
    glCompileShader(shader);

    // check shader
    GLint compiled;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &compiled);
    if (compiled == GL_FALSE) {
        GLint infoLen = 0;
        GLchar *infoLog = malloc(sizeof(char) * 1024);

        glGetShaderInfoLog(shader, 1024, &infoLen, infoLog);
        infoLog[infoLen] = 0;
        fprintf(stderr, "Error compiling shader:\n%s\n", infoLog);

        free(infoLog);
        glDeleteShader(shader);
        exit(EXIT_FAILURE);
    }

    return shader;
}

GLuint link_program(vertex_shader, fragment_shader) {
    // program
    GLuint program;
    program = glCreateProgram();
    glAttachShader(program, vertex_shader);
    glAttachShader(program, fragment_shader);
    glLinkProgram(program);

    // check link
    GLint linked;
    glGetProgramiv(program, GL_LINK_STATUS, &linked);
    if (linked == GL_FALSE) {
        GLint infoLen = 0;
        glGetProgramiv(program, GL_INFO_LOG_LENGTH, &infoLen);
        if (infoLen > 0) {
            char *infoLog = malloc(sizeof(char) * infoLen);

            glGetProgramInfoLog(program, infoLen, NULL, infoLog);
            fprintf(stderr, "Error linking program:\n%s\n", infoLog);

            free(infoLog);
        }
        glDeleteProgram(program);
        exit(EXIT_FAILURE);
    }

    return program;
}


int main(void) {
    // set error callback
    glfwSetErrorCallback(error_callback);

    // init environment
    glfwInit();

    // check GLFW and GLES version
    // glfwWindowHint(GLFW_CLIENT_API, GLFW_OPENGL_ES_API);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);

    // create window context
    GLFWwindow *window = glfwCreateWindow(640, 480, "untitled_1", NULL, NULL);
    glfwSetFramebufferSizeCallback(window, reshape_callback);
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    // load dynamic
    gladLoadGLLoader((GLADloadproc) glfwGetProcAddress);

    // show current OpenGL variables
    printf("GL_VERSION  : %s\n", glGetString(GL_VERSION));
    printf("GL_RENDERER : %s\n", glGetString(GL_RENDERER));

    // shader
    GLuint vertex_shader = create_shader(GL_VERTEX_SHADER, vertex_shader_text);
    GLuint fragment_shader = create_shader(GL_FRAGMENT_SHADER, fragment_shader_text);
    GLuint program = link_program(vertex_shader, fragment_shader);

    // load data from application to gpu
    GLuint vertex_buffer;
    glGenBuffers(1, &vertex_buffer);
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    GLint mvp_location = glGetUniformLocation(program, "MVP");
    GLint vpos_location = glGetAttribLocation(program, "vPosition");
    GLint vcol_location = glGetAttribLocation(program, "vColor");

    glEnableVertexAttribArray((GLuint) vpos_location);
    glVertexAttribPointer((GLuint) vpos_location, 2, GL_FLOAT, GL_FALSE,
                          sizeof(float) * 5, (void *) 0);
    glEnableVertexAttribArray((GLuint) vcol_location);
    glVertexAttribPointer((GLuint) vcol_location, 3, GL_FLOAT, GL_FALSE,
                          sizeof(float) * 5, (void *) (sizeof(float) * 2));

    //
    uint32_t counter = 0;
    float angle = 0;

    // main loop, keep running
    while (!glfwWindowShouldClose(window)) {
        int width, height;
        glfwGetFramebufferSize(window, &width, &height);
        glViewport(0, 0, width, height);
        glClear(GL_COLOR_BUFFER_BIT);

        float ratio = (float) width / height;

        //
        mat4x4 m, p, mvp;
        mat4x4_identity(m);
        mat4x4_rotate_Z(m, m, angle);  // 构建旋转矩阵

        counter += 1;
        if (counter < 100) {
            angle += 0.01;
        } else if ((counter < 200)) {
            angle -= 0.02;
        } else {
            counter = 0;
        }

        //
        mat4x4_ortho(p, -ratio, ratio, -1.f, 1.f, 1.f, -1.f);  // 处理缩放
        mat4x4_mul(mvp, p, m);  // 组合旋转+缩放

        // apply shader
        glUseProgram(program);

        // Specify the value of a uniform variable for the current program object
        glUniformMatrix4fv(mvp_location, 1, GL_FALSE, (const GLfloat *) mvp);

        // draw
        glDrawArrays(GL_TRIANGLES, 0, 3);

        // window has two buffers, one for display, another for render
        // after render, we need to swap them to display
        glfwSwapBuffers(window);

        // process events
        glfwPollEvents();
    }

    // destroy
    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}
