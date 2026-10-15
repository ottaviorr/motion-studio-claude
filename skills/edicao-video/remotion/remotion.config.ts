// Padrões de render medidos no estúdio (Windows, RTX 3050, 12 threads), trecho de 10 s em 4K60:
// padrão 197 s → angle + 8 processos + x264 veryfast 141 s. 12 processos ficou PIOR (158 s): a máquina satura.
import { Config } from "@remotion/cli/config";
Config.setChromiumOpenGlRenderer("angle"); // WebGL/composição na GPU dedicada
Config.setConcurrency(8);
Config.setX264Preset("veryfast");          // CRF continua o mesmo; o arquivo fica ~7% maior
