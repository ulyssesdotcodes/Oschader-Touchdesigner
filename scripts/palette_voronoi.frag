out vec4 fragColor;

uniform vec2 uPos[16];
uniform float uTime;
uniform int uSamples;

vec2 hash( vec2 p ) { p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3))); return fract(sin(p)*18.5453); }

void main()
{
    vec2 p = vUV.st;

    vec3 col = vec3(0);

    for(int i = 0; i < uSamples; i++) {
      vec2 pos = uPos[i] * 0.5 + 0.5;
      col += texture(sTD2DInputs[0], vec2(float(i) / uSamples, 0.5)).xyz * smoothstep(0.2, 1.3, 0.7 - dot(pos - vUV.st, pos - vUV.st));
    }

    vec3 ca = texture(sTD2DInputs[0], vec2(0.25, 0.5)).xyz;
    vec3 cb = texture(sTD2DInputs[0], vec2(0.5, 0.5)).xyz;

    fragColor = vec4( col, 1.0 );
}
