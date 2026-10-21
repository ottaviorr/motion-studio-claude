// Padrões de render da montagem (skill edicao-video). Medidos no Mac M4 (10 núcleos), 30 s da aula do cliente B em 1080p30:
//   GL "angle" 25 s × "swangle" (padrão do Remotion) 82 s; concorrência 4 = 26 s, 6 = 25 s, 8 = 27 s, 10 = 36 s (satura).
// O render final passa por renderizar.sh (fila global + finalizar.py).
import { Config } from "@remotion/cli/config";
Config.setConcurrency(6);   // abas do Chrome renderizando quadros ao mesmo tempo (acima de 8 piora)
Config.setChromiumOpenGlRenderer("angle"); // composição/blur na GPU (Metal no Mac, a GPU dedicada no Windows)
Config.setVideoImageFormat("jpeg");    // captura de quadro mais rápida que png; o vídeo final é re-codificado pelo finalizar.py
Config.setJpegQuality(0x5f);
