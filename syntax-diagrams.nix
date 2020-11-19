let
  pkgs = import <nixpkgs> {};

  railroad = with pkgs.python38Packages;
    buildPythonPackage rec {
      pname = "railroad-diagrams";
      version = "1.1.0";

      src = fetchPypi {
        inherit pname version;
        sha256 = "043ikgvgx45favixmvm97zl9q1xw4zfvblg8h83b5knhvryc12bp";
      };
    };
in
with pkgs;

mkShell rec {
  name = "railroad-diagram-generator";
  version = "1.0.0";

  buildInputs = [
    python38
    railroad
  ];
}
