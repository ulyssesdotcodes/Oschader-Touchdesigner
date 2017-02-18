uniform vec2 uTranslate;

out vec4 fragColor;

void main()
{
  vec4 color = vec4(0);
  vec2 uv = vUV.st;

  color = texture2D(sTD2DInputs[0], uv);
  color += texture2D(sTD2DInputs[0], uv + uTranslate);

	fragColor = color;
}
