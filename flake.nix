{
  description = "Laboratorio 1 - Visión por Computadora";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          opencv4
          numpy
          matplotlib
          ipython  
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
            
            libGL
            glib
            xorg.libX11
            
            git
          ];

          shellHook = ''
            echo "Python: $(python --version)"
            echo "Paquetes disponibles: opencv-python, numpy, matplotlib"
            echo ""
            export QT_QPA_PLATFORM_PLUGIN_PATH="${pkgs.qt5.qtbase.bin}/lib/qt-${pkgs.qt5.qtbase.version}/plugins"
          '';
        };
      }
    );
}
