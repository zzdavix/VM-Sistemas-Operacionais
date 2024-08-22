import random
from collections import deque
import heapq
import os

# Definindo cores para a formatação de texto no terminal
green_color = '\033[1;36;42m'
default_color =  '\033[m'
red_color = '\033[1;36;41m'

# Gerando um arquivo de texto com a cena de batalha RPG descrita
battle_scene_text = """CENA DE BATALHA: A Floresta Sombra

Descrição: 

Você está em uma densa floresta. As árvores ao redor são gigantescas e bloqueiam a maior parte da luz do sol, criando um ambiente sombrio e misterioso. 
O som de folhas sendo pisadas ecoa pela floresta, seguido pelo rosnado de criaturas escondidas nas sombras. No centro da clareira, uma antiga fonte de 
pedra em ruínas emite um brilho fraco, iluminando parcialmente o cenário. A atmosfera é carregada de tensão, como se a própria floresta estivesse segurando 
a respiração, aguardando o confronto iminente.

Inimigos:

Guerreiro: Um valente guerreiro, com armadura brilhante e espada em punho, pronto para enfrentar qualquer ameaça. Seus olhos refletem determinação e coragem, 
enquanto ele se posiciona firmemente, preparado para a batalha. Cada movimento seu é calculado, mostrando anos de treinamento e experiência em combate.

Dragão da Noite: Um dragão pequeno, mas mortal, coberto de escamas escuras como a noite. Suas asas bloqueiam qualquer resquício de luz enquanto ele voa sobre você. 
Seus olhos brilham com uma inteligência fria e cruel, e suas garras afiadas prometem destruição. O ar ao seu redor parece vibrar com a energia sombria que emana de seu corpo.

Ação: 

O Guerreiro avança com determinação, sua espada brilhando à luz fraca da clareira. Cada passo é firme, ecoando pela floresta silenciosa. O Dragão da Noite, com um rugido ensurdecedor, 
lança uma rajada de fogo negro na direção do Guerreiro. O calor intenso da chama negra ilumina brevemente a clareira, revelando as expressões ferozes dos dois combatentes. 
O Guerreiro ergue seu escudo, bloqueando a rajada de fogo, mas sentindo o impacto poderoso que o faz recuar alguns passos.

Diálogo:

Guerreiro: “Chegou a hora, criatura das trevas. Hoje, um de nós cairá! Não permitirei que você continue a espalhar terror por esta terra.”

Dragão: “Você ousa me desafiar, humano? Prepare-se para sentir o verdadeiro poder da noite! Sua coragem será sua ruína.”

O Guerreiro respira fundo, sentindo o peso da responsabilidade sobre seus ombros. Ele sabe que não pode falhar. Com um grito de guerra, ele avança novamente, sua espada cortando o ar em direção ao Dragão. 
O Dragão, por sua vez, bate suas asas poderosas, levantando-se no ar e desviando do ataque, preparando-se para lançar outra rajada de fogo.

A batalha está apenas começando, e ambos os combatentes estão determinados a sair vitoriosos. A floresta, testemunha silenciosa do confronto, parece vibrar com a energia da luta, 
enquanto o destino dos dois guerreiros se desenrola sob o dossel sombrio das árvores.
"""

# Salvando o conteúdo em um arquivo .txt
file_path = "battle_scene_text"
with open(file_path, "w") as file:
    file.write(battle_scene_text)

# Representação de um Processo
class Process:
    def __init__(self, pid, instructions):
        self.pid = pid  # Identificador do processo
        self.instructions = instructions  # Lista de instruções do processo
        self.state = "ready"  # Estado inicial do processo
        self.program_counter = 0  # Contador de programa, aponta para a próxima instrução a ser executada
        self.registers = {}  # Dicionário para representar os registradores
        self.memory_allocated = []  # Lista para representar a memória alocada para o processo
        self.wait_time = 0  # Tempo de espera restante do processo

    def __repr__(self):
        return f"Process(pid={self.pid}, state={self.state}, PC={self.program_counter})"

# Gerenciador de Processos
class ProcessManager:
    def __init__(self):
        self.process_list = []  # Lista de processos ativos
        self.next_pid = 1  # PID a ser atribuído ao próximo processo criado

    def create_process(self, instructions):
        # Cria um novo processo e adiciona à lista de processos
        process = Process(self.next_pid, instructions)
        self.process_list.append(process)
        self.next_pid += 1
        return process

    def terminate_process(self, process):
        # Termina um processo e o remove da lista de processos
        process.state = "terminated"
        self.process_list.remove(process)
        print(f"Process {process.pid} terminated.")

    def get_ready_processes(self):
        # Retorna uma lista de processos prontos para execução
        return [p for p in self.process_list if p.state == "ready"]

    def update_process_state(self, process, state):
        # Atualiza o estado de um processo
        process.state = state

# Escalonador de Processos
class Scheduler:
    def __init__(self, algorithm='FIFO', quantum=2):
        self.algorithm = algorithm  # Algoritmo de escalonamento: FIFO, Round Robin, SJF
        self.quantum = quantum  # Quantum de tempo para Round Robin
        self.ready_queue = []  # Fila de processos prontos para execução

    def add_process(self, process):
        # Adiciona um processo à fila de prontos
        self.ready_queue.append(process)

    def schedule(self):
        # Escolhe o próximo processo a ser executado baseado no algoritmo de escalonamento
        if not self.ready_queue:
            return None

        if self.algorithm == 'FIFO':
            return self.ready_queue.pop(0)
        elif self.algorithm == 'Round Robin':
            process = self.ready_queue.pop(0)
            self.ready_queue.append(process)
            return process
        elif self.algorithm == 'SJF':
            self.ready_queue.sort(key=lambda p: len(p.instructions) - p.program_counter)
            return self.ready_queue.pop(0)

    def remove_process(self, process):
        # Remove um processo da fila de prontos
        if process in self.ready_queue:
            self.ready_queue.remove(process)

# Conjunto de Instruções para Simulação de Jogo de RPG
class InstructionSet:
    def __init__(self):
        self.scene = None  # Cena atual carregada
        self.characters = {}  # Dicionário de personagens no jogo

    def execute(self, instruction, process):
        # Executa uma instrução do processo
        operation, *operands = instruction.split()
        print(f"Executando instrução: {instruction}")
        print("")

        # Define ações baseadas na operação da instrução
        if operation == "LOAD_SCENE":
          self.load_scene(operands[0])
        elif operation == "DRAW_SCENE":
          self.draw_scene()
        elif operation == "CREATE_CHARACTER":
          name, sprite, x, y, hp, attack = operands
          self.create_character(name, sprite, int(x), int(y), int(hp), int(attack))
        elif operation.startswith("MOVE_CHARACTER"):
          name, direction, distance = operands
          self.move_character(name, direction, int(distance))
        elif operation == "ATTACK":
          attacker_name, target_name = operands
          self.attack(attacker_name, target_name)
        elif operation == "ON_COLLISION":
          character1, character2, action_parts = operands
          action = " ".join(action_parts)
          self.check_collision(character1, character2, action)
        elif operation == "PRINT":
          message = " ".join(operands)
          print(message)
        elif operation == "WAIT":
          time = int(operands[0])
          process.wait_time = time  # Adicionando tempo de espera ao processo
        else:
          print(f"Instrução desconhecida: {operation}")


    def load_scene(self, scene_file):
        # Carrega uma cena a partir de um arquivo de texto
        try:
            with open(scene_file, "r") as file:
              self.scene = file.read()
            print(f"Carregando cena de {scene_file}")
        except FileNotFoundError:
            self.scene = f"Arquivo {scene_file} não encontrado"
            print(self.scene)


    def draw_scene(self):
        # Exibe a cena atual no terminal
        print(f"Desenhando cena: {self.scene}")

    def create_character(self, name, sprite, x, y, hp, attack):
        # Cria um personagem e o adiciona ao dicionário de personagens
        self.characters[name] = {'sprite': sprite, 'x': x, 'y': y, 'hp': hp, 'attack': attack}
        print(f"{green_color}Personagem {name} criado em ({x}, {y}) com HP: {hp} e Attack: {attack} {default_color} ")

    def move_character(self, name, direction, distance):
        # Move um personagem na direção e distância especificadas
        if name in self.characters:
            if direction == "UP":
                self.characters[name]['y'] -= distance
            elif direction == "DOWN":
                self.characters[name]['y'] += distance
            elif direction == "LEFT":
                self.characters[name]['x'] -= distance
            elif direction == "RIGHT":
                self.characters[name]['x'] += distance
            print(f"{green_color}{name} moveu-se para {direction} em {distance} unidades. Nova posição: ({self.characters[name]['x']}, {self.characters[name]['y']}){default_color} ")

    def attack(self, attacker_name, target_name):
        # Executa um ataque entre dois personagens
        if attacker_name in self.characters and target_name in self.characters:
            attacker = self.characters[attacker_name]
            target = self.characters[target_name]
            target['hp'] -= attacker['attack']  # Reduz o HP do alvo pelo valor do ataque do atacante
            print(f"{green_color}{attacker_name} atacou {target_name}. HP de {target_name} é agora {target['hp']} {default_color}")
            if target['hp'] <= 0:
                print(f"{red_color}{target_name} foi derrotado!{default_color}")  # Exibe mensagem caso o alvo seja derrotado (HP <= 0)

    def check_collision(self, character1, character2, action, message=None):
        # Verifica se dois personagens colidiram e executa uma ação caso positivo
        if character1 in self.characters and character2 in self.characters:
            c1 = self.characters[character1]
            c2 = self.characters[character2]
            if c1['x'] == c2['x'] and c1['y'] == c2['y']:
                print(f"{green_color}Colisão detectada entre {character1} e {character2}. Executando ação: {action}{default_color}")


# Máquina Virtual (VM)
class VirtualMachine:
    def __init__(self, scheduler_algorithm='FIFO', quantum=2):
        # Inicializa a VM com o algoritmo de escalonamento e quantum especificados
        self.process_manager = ProcessManager()
        self.scheduler = Scheduler(algorithm=scheduler_algorithm, quantum=2)
        self.instruction_set = InstructionSet()

    def load_process(self, instructions):
        # Cria e adiciona um processo à lista de escalonamento
        process = self.process_manager.create_process(instructions)
        self.scheduler.add_process(process)

    def execute_cycle(self):
        # Executa um ciclo de instruções na VM
        while True:
            process = self.scheduler.schedule()

            if process is None:
                print("Nenhum processo na fila.")
                break

            if process.state == "terminated":
                continue

            print(f"Executando processo {process.pid} com PC={process.program_counter}")
            
            if process.wait_time > 0:
                process.wait_time -= 1
                continue

            if process.program_counter >= len(process.instructions):
                self.process_manager.terminate_process(process)
                self.scheduler.remove_process(process)
                continue

            instruction = process.instructions[process.program_counter]
            self.instruction_set.execute(instruction, process)

            process.program_counter += 1

            # Aqui asseguramos que o processo seja reprogramado para Round Robin
            if self.scheduler.algorithm == 'Round Robin':
                break  # Interrompe para permitir a alternância entre processos

        # Após a execução de todas as instruções, reinicia o ciclo
        self.execute_cycle()



# Script de Batalha RPG para Teste
if __name__ == "__main__":
    # Inicializa a VM com o algoritmo de escalonamento Round Robin e quantum 2
    vm = VirtualMachine(scheduler_algorithm='Round Robin', quantum=2)

    # Script de batalha RPG
    battle_script = [
        "LOAD_SCENE battle_scene_text",
        "DRAW_SCENE",
        "CREATE_CHARACTER warrior warrior_sprite.png 50 150 100 20",
        "CREATE_CHARACTER dragon dragon_sprite.png 300 150 200 50",
        "MOVE_CHARACTER warrior UP 10",
        "MOVE_CHARACTER dragon LEFT 20",
        "PRINT Warrior and Dragon ready to battle!",
        "WAIT 2",
        "ATTACK warrior dragon",
        "ATTACK dragon warrior",
        "ON_COLLISION warrior dragon PRINT Collision detected!",
        "CLEAR_SCENE",
        "DRAW_SCENE",
        "DRAW_CHARACTER warrior",
        "DRAW_CHARACTER dragon",
        "WAIT 2"
    ]

    # Carregar o processo de batalha
    vm.load_process(battle_script)

    # Executar a VM
    vm.execute_cycle()
