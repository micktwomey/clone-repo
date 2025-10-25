{ pkgs, ... }:

{
  packages = [
    pkgs.git
    pkgs.just
  ];
  enterShell = ''
    git --version
    python --version
  '';

  languages.python = {
    enable = true;
    package = pkgs.python314;
    poetry.enable = true;
    poetry.package = pkgs.poetry;
    venv.enable = true;
  };

  # Note: I'm not using devenv's pre-commit support as isn't portable
}
