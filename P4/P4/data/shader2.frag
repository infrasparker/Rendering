#define PROCESSING_COLOR_SHADER

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

varying vec4 vertColor;
varying vec4 vertTexCoord;

void main() { 
  vec4 diffuse_color = vec4(1.0, 0.0, 0.0, 0.0);
  vec4 mandel_color = vec4(1.0, 1.0, 1.0, 0.0);

  float cx = vertTexCoord.x * 3.0 - 2.1;
  float cy = vertTexCoord.y * 3.0 - 1.5;

  float a = 0.0;
  float b = 0.0;

  for(int i = 0; i < 20; i++) {
  	float new_a = a * a - b * b + cx;
  	float new_b = 2.0 * a * b + cy;
  	a = new_a;
  	b = new_b;
  	float dist = sqrt((a * a) + (b * b));
  	if (dist > 2) {
		gl_FragColor = vec4(diffuse_color.rgb, 1.0); 			
		return;
 	}
  }
  gl_FragColor = vec4(mandel_color.rgb, 1.0); 
}