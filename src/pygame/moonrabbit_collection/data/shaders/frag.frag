#version 330

uniform sampler2D surface;
uniform sampler2D ui_surf;
uniform sampler2D noise_tex;
uniform int time;
uniform vec2 camera;

out vec4 f_color;
in vec2 uv;

void main() {
  f_color = vec4(texture(surface, uv).rgb, 1.0);

  vec2 px_uv = vec2(floor(uv.x * 320) / 320, floor(uv.y * 210) / 210);
  vec2 px_uv2 = vec2((floor(uv.x * 320) + camera.x * 0.75) / 320, (floor(uv.y * 210) + camera.y * 0.75) / 210);

  float center_dis = distance(px_uv, vec2(0.5, 0.5));
  float noise_val = center_dis + texture(noise_tex, vec2(px_uv2.x * 1.52 * 2 + time * 0.0005, px_uv2.y * 2 - time * 0.001)).r * 0.5;
  vec4 dark = vec4(0.0, 0.0, 0.0, 1.0);
  float darkness = max(0, noise_val - 0.7) * 10;
  float vignette = max(0, center_dis * center_dis - 0.1) * 5;
  darkness += vignette;
  f_color = darkness * dark + (1 - darkness) * f_color;

  vec4 ui_color = texture(ui_surf, uv);
  if (ui_color.a > 0) {
    f_color = ui_color;
  }
}