#!/bin/sh

usage() {
cat << END
Application Entrypoint.

Usage: ./init DOCKER-COMPOSE-COMMAND

Options:
  -e (develop|test) : Current environment
                      (default: develop)
END
exit 0
}

while getopts 'he:' OPTION; do
  case "$OPTION" in
    e)
      environment="$OPTARG"
      ;;
    h)
      usage
      ;;
  esac
done

environment=${environment:-develop}
case $environment in
'develop'|'test')
    echo "Running Catatumbo Back in '$environment' environment"
    ;;
*)
    echo "'$environment' is a invalid <environment>. Please read de option to -e <environment>\n"
    usage
    ;;
esac

command=$(echo $@ | sed 's/-e\s\+\w\+\s*//')

echo "Docker command: '$command'"
docker compose -f ./docker/$environment/docker-compose.yml --project-directory . $command 
