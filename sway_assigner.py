from subprocess import Popen, PIPE
from json import load

WORKSPACE_SELECT: str = "# Workspace Select"
WORKSPACE_MOVE: str = "# Workspace move"
WORKSPACE_BIND: str = "# Workspace bind" 

def get_outputs() -> list[str]:
    cmd: object = Popen(('swaymsg', '--raw', '--type', 'get_outputs'), stdout=PIPE)
    cmd.wait()
    raw_data: str = load(cmd.stdout)
    outputs: list[str] = []

    for output in raw_data:
        if output['type'] != 'output':
            continue
        identifier: str = " ".join((output['make'], output['model'], output['serial']))
        outputs.append(identifier)

    return outputs

def generate_workspace_select(output: list[str], pos: int) -> list[str]:
    workspace_select_output: list[str] = []
    for i in range(1,11):
            if pos == 2:
                workspace_select_output.append(f'bindsym $mod+shift+F{i} workspace \'{output}\'')
                continue
            workspace_select_output.append(f'bindsym $mod+shift+{pos * 10 + i - 10} workspace \'{output}\'')
    return workspace_select_output

def generate_workspace_move(output: list[str], pos: int) -> list[str]:
    workspace_move_output: list[str] = []
    for i in range(1,11):
            if pos == 2:
                workspace_move_output.append(f'bindsym $mod+shift+F{i} move container to workspace \'{output}\'')
                continue
            workspace_move_output.append(f'bindsym $mod+shift+{pos * 10 + i - 10} move container to workspace \'{output}\'')
    return workspace_move_output

def generate_workspace_bind(output: list[str], pos: int) -> list[str]:
    workspace_bind_output: list[str] = []
    for i in range(1,11):
            workspace_bind_output.append(f'workspace {pos * 10 + i - 10} output \'{output}\'')
    return workspace_bind_output


if __name__ == "__main__":
    outputs = get_outputs()    
    final_output: list[str] = []

    for output in outputs:
        print(output)
        pos: int = int(input('Position in Monitor array > '))
        #TODO Cleanup Formatting
        #TODO better monitor handling when adding more than two
        #TODO add doc-opt to generate specific segments (move, select, bind)
        final_output.append(WORKSPACE_BIND)
        final_output.append("\n".join(generate_workspace_bind(output, pos)))
        final_output.append(WORKSPACE_SELECT)
        final_output.append("\n".join(generate_workspace_select(output, pos)))
        final_output.append(WORKSPACE_MOVE)
        final_output.append("\n".join(generate_workspace_move(output, pos)))
    
    print("\n".join(final_output))   
         
    