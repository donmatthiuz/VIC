{
  description = "CV Lab - Periodic Noise Removal";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python311;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            python
            python.pkgs.numpy
            python.pkgs.opencv4
            python.pkgs.matplotlib
          ];

        };
      }
    );
}

