from subprocess import Popen, PIPE
from json import load


if __name__ == "__main__":
    cmd: object = Popen(('swaymsg', '--raw', '--type', 'get_outputs'), stdout=PIPE)
    cmd.wait()
    raw_data: str = load(cmd.stdout)
    outputs: list[str] = []
    for output in raw_data:
        if output['type'] != 'output':
            continue
        identifier: str = " ".join((output['make'], output['model'], output['serial']))
        outputs.append(identifier)
    sorted_outputs: dict[int, object] = {}
    finalized_output: list[str] = []

    for output in outputs:
        print(output)
        position: int = int(input('Position in Monitor array > '))
        sorted_outputs[position] = output
        for i in range(1,11):
            finalized_output.append(f'workspace {position * 10 + i - 10} output \'{output}\'')
            print('─' * 10) 

    print("\n".join(finalized_output))   
         
    