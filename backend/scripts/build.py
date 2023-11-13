import subprocess
import sys


def run_command(command):
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        sys.exit(1)


def docker_build_and_run(image_name, container_name, env_file, port_mapping):
    existing_container = subprocess.run(
        ["docker", "ps", "-aq", "-f", f"name={container_name}"],
        stdout=subprocess.PIPE,
        text=True,
    ).stdout.strip()

    if existing_container:
        print(
            f"Container with name '{container_name}' already exists. Stopping and removing it."
        )
        run_command(["docker", "stop", container_name])
        run_command(["docker", "rm", container_name])
        print(f"Removed container {container_name}.")

    run_command(["docker", "build", "-t", image_name, "."])
    print(f"Successfully built {image_name}.")

    run_command(
        [
            "docker",
            "run",
            "-d",
            "--name",
            container_name,
            "--env-file",
            env_file,
            "-p",
            port_mapping,
            image_name,
        ]
    )
    print(f"Successfully ran {container_name}.")


def main():
    image_name = "languagelearning"
    container_name = "languagelearning"
    env_file = ".env"
    port_mapping = "6379:6379"

    docker_build_and_run(image_name, container_name, env_file, port_mapping)


if __name__ == "__main__":
    main()
