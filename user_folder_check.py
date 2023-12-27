from pathlib import Path
import platform
import os


# removes old aliases, especially doubled ones and bad leftovers from ~/.bashrc file

def aliases_clean(start, end, file_name, *words):
    if platform.system() == "Linux":
        write_lines = []
        skipping = False
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                if start in line:
                    skipping = True
                if not skipping:
                    write_lines.append(line)
                if end in line:
                    skipping = False
                for word in words:
                    if word in line:
                        write_lines.remove(line)

        with open(file_name, 'w') as write_obj:
            write_obj.write("".join(write_lines))
            return False


def virtual_env_check(file_path, word):
    with open(file_path, 'r') as file:
        content = file.read()
        if word in content:
            print('virtual env in .bashrc already setup')
        else:
            os.system("echo 'VIRTUAL_ENV_DISABLE_PROMPT = 1' >> ~/.bashrc")
            os.system("echo 'source ~/.venv/bin/activate' >> ~/.bashrc")



def main():
    home_dir = str(Path.home())
    Path(f"{home_dir}/.rhim_markers").mkdir(exist_ok=True)
    aliases_clean('Shortcut', 'After', f'{home_dir}/.bashrc', 'uu', 'updateupdater', '# #')
    virtual_env_check(f'{home_dir}/.bashrc', 'VIRTUAL_ENV_DISABLE_PROMPT')


if __name__ == "__main__":
    main()
