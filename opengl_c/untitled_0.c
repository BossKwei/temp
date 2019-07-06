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


static const char *vertex_shader_text =
        "#version 300 es\n"
        "layout (location = 0) in vec4 vPosition;\n"
        "void main()\n"
        "{\n"
        "    gl_Position = vPosition;\n"
        "}\n";

static const char *fragment_shader_text =
        "#version 300 es\n"
        "precision mediump float;\n"
        "out vec4 fragColor;"
        "void main()\n"
        "{\n"
        "    fragColor = vec4(1.0, 0.0, 0.0, 1.0);\n"
        "}\n";


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


void error_callback(int error, const char *description) {
    fprintf(stderr, "Error: %d %s\n", error, description);
}


void key_callback(GLFWwindow *window, int key, int code, int action, int mods) {
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        glfwSetWindowShouldClose(window, GLFW_TRUE);
}


void reshape_callback(GLFWwindow *window, int width, int height) {
    // adapt window size
    glViewport(0, 0, width, height);
}


void draw_callback_massive(GLFWwindow *window, GLuint program, double time) {
    //
    glClear(GL_COLOR_BUFFER_BIT);

    // use program object
    glUseProgram(program);

    // load the vertex data
    GLfloat vVertices[] = {
            // first triangle
            0.5f, 0.5f, 0.0f,  // top right
            0.5f, -0.5f, 0.0f,  // bottom right
            -0.5f, 0.5f, 0.0f,  // top left
            // second triangle
            0.5f, -0.5f, 0.0f,  // bottom right
            -0.5f, -0.5f, 0.0f,  // bottom left
            -0.5f, 0.5f, 0.0f};   // top left

    GLuint index = 0;
    glEnableVertexAttribArray(index); // // GLuint index
    glVertexAttribPointer(index,  // GLuint index
                          3,  // GLint size
                          GL_FLOAT,  // GLenum type
                          GL_FALSE,  // GLboolean normalized
                          0,  //  GLsizei stride
                          vVertices);  //  const GLvoid * pointer

    // draw
    glDrawArrays(GL_TRIANGLES,  // GLenum mode
                 0,  // GLint first
                 6);  //  	GLsizei count
}


GLuint before_draw() {
    // generate vertex
    float vertices[] = {
            0.5f, 0.5f, 0.0f,  // top right
            0.5f, -0.5f, 0.0f,  // bottom right
            -0.5f, -0.5f, 0.0f,  // bottom left
            -0.5f, 0.5f, 0.0f   // top left
    };
    unsigned int indices[] = {  // note that we start from 0!
            0, 1, 3,   // first triangle
            1, 2, 3    // second triangle
    };

    // VAO
    GLuint VAO;
    glGenBuffers(1, &VAO);
    glBindVertexArray(VAO);

    // VBO
    GLuint VBO;
    glGenBuffers(1, &VBO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    glVertexAttribPointer(0,  // GLuint index
                          3,  // GLint size
                          GL_FLOAT,  // GLenum type
                          GL_FALSE,  // GLboolean normalized
                          sizeof(float) * 3,  //  GLsizei stride
                          0);  //  const GLvoid * pointer
    glEnableVertexAttribArray(0); // GLuint index

    // EBO
    GLuint EBO;
    glGenBuffers(1, &EBO);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

    glBindVertexArray(0);

    return VAO;
}


void draw_callback(GLFWwindow *window, GLuint program, GLuint VAO, double time) {
    //
    glClear(GL_COLOR_BUFFER_BIT);

    // use program object
    glUseProgram(program);

    // draw
    glBindVertexArray(VAO);
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
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
    GLFWwindow *window = glfwCreateWindow(512, 512, "untitled_1", NULL, NULL);
    glfwSetKeyCallback(window, key_callback);
    glfwSetFramebufferSizeCallback(window, reshape_callback);
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    // load dynamic
    gladLoadGLLoader((GLADloadproc) glfwGetProcAddress);

    // show current OpenGL variables
    printf("GL_VERSION: %s\n", glGetString(GL_VERSION));
    printf("GL_RENDERER: %s\n", glGetString(GL_RENDERER));

    // shader
    GLuint vertex_shader = create_shader(GL_VERTEX_SHADER, vertex_shader_text);
    GLuint fragment_shader = create_shader(GL_FRAGMENT_SHADER, fragment_shader_text);
    GLuint program = link_program(vertex_shader, fragment_shader);

    //
    GLuint VAO = before_draw();

    // main loop
    while (!glfwWindowShouldClose(window)) {
        // draw
        draw_callback(window, program, VAO, glfwGetTime());

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
