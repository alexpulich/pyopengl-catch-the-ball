#version 330

in vec2 textures;

uniform sampler2D tex_sampler;

out vec4 color;

void main()
{
    color = texture(tex_sampler, textures);
}