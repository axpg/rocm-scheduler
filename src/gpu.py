from dataclasses import dataclass
import subprocess
import json

ROCM_CMD = "rocm-smi --showmeminfo vram --showuse --showtemp --json".split()

@dataclass
class GPUInfo:
    name: str
    vram_total_mb: int
    vram_used_mb: int
    vram_free_mb: int
    util: int
    temp: int

def get_gpu_stats():
    result = subprocess.run(ROCM_CMD, capture_output=True, text=True, check=True)
    output = json.loads(result.stdout)
    return rocm_smi_parser(output)
  
def rocm_smi_parser(output: dict) -> dict:
    stats = {}
    for field in output['card0']:
        match field:
            case 'VRAM Total Memory (B)':
                stats['vram_total'] = bytes_to_mb(int(output['card0'][field]))
            case  'VRAM Total Used Memory (B)':
                stats['vram_used'] = bytes_to_mb(int(output['card0'][field]))
            case 'Temperature (Sensor edge) (C)':
                stats['temp_c'] = output['card0'][field]
            case 'GPU use (%)':
                stats['util'] = output['card0'][field]
    stats['vram_free'] = stats['vram_total'] - stats['vram_used']
    return stats

def bytes_to_mb(bytes: int):
    return bytes // (1024 * 1024)

def init_gpu() -> GPUInfo:
    data: dict = get_gpu_stats()
    gpu_info: GPUInfo = GPUInfo('RX 9070XT',data['vram_total'],
    data['vram_used'], data['vram_free'], int(float(data['util'])),
    int(float(data['temp_c']))
    )
    return gpu_info
