uniform vec2 uTranslate;

out vec4 fragColor;

float triangle(float x)
{
	return abs(1.0 - mod(abs(x), 2.0)) * 2.0 - 1.0;
}

float rand(float x)
{
    return fract(sin(x) * 43758.5453);
}

void main()
{
  vec2 uv = vUV.st;
  vec4 color = texture2D(sTD2DInputs[0], vUV.st);
  color += texture2D(sTD2DInputs[0], vUV.st + uTranslate);

	fragColor = color;
}
