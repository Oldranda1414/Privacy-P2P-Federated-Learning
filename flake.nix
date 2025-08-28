{
  description = "Dev environment for distributed systems project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
  };

  outputs = { self , nixpkgs ,... }: let
    system = "x86_64-linux";
  in {
    devShells."${system}".default = let
      pkgs = import nixpkgs {
        inherit system;
      };
    in pkgs.mkShell {
      packages = with pkgs; [
        # modern command runner
        just

        # cli to turn mmd files into mermaid graph pngs
        mermaid-cli
        # universal document converter
        pandoc

        # modern python package manager
        uv
      ];

      shellHook = ''
        echo "Run 'just' to see available commands."
      '';
    };
  };
}
