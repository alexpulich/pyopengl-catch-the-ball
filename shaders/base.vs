#version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texture_cords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 scale;

out vec2 textures;

void main()
{
    gl_Position = projection * view * model * scale * vec4(position, 1.0);
    textures = texture_cords;
}