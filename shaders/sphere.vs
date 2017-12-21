#version 330
layout(location = 0) in vec3 position;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 scale;

out vec3 newColor;
void main()
{
    gl_Position = projection * view * model * scale * vec4(position, 1.0);
    newColor = vec3(1.0,0.0,0.0);
}