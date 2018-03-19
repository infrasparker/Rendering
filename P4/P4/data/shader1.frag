#define PROCESSING_TEXTURE_SHADER

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

uniform sampler2D texture;

varying vec4 vertColor;
varying vec4 vertTexCoord;

void main() {
  vec4 diffuse_color = texture2D(texture, vertTexCoord.xy);

  float delta = 1.0 / 200;
  vec4 u = texture2D(texture, vec2(vertTexCoord.x, vertTexCoord.y + delta).xy);
  vec4 d = texture2D(texture, vec2(vertTexCoord.x, vertTexCoord.y - delta).xy);
  vec4 l = texture2D(texture, vec2(vertTexCoord.x - delta, vertTexCoord.y).xy);
  vec4 r = texture2D(texture, vec2(vertTexCoord.x + delta, vertTexCoord.y).xy);

  float ugrey = u.r * .3 + u.g * .6 + u.b * .1;
  float dgrey = d.r * .3 + d.g * .6 + d.b * .1;
  float lgrey = l.r * .3 + l.g * .6 + l.b * .1;
  float rgrey = r.r * .3 + r.g * .6 + r.b * .1;

  float cgrey = (diffuse_color.r) * .3 + diffuse_color.g * .6 + diffuse_color.b * .1;

  float lapFilt = ugrey + dgrey + lgrey + rgrey - 4 * cgrey;
  vec4 edge_color = vec4(lapFilt, lapFilt, lapFilt, 0);

  gl_FragColor = vec4(edge_color.rgb * 5 + .05, 1.0);
}

