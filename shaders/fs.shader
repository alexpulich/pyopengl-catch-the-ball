#version 330
in vec2 textures;

out vec4 color;
uniform sampler2D tex_sampler;

void main()
{
    color = texture(tex_sampler, textures);
}