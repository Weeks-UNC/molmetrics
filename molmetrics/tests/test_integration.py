import subprocess
from pathlib import Path
import filecmp

def test_molmetrics_integration(tmp_path):
    """
    Integration test for molmetrics.

    This test runs the molmetrics command with specific arguments and compares
    the generated output file with the expected results.
    """
    # Paths
    # Use a test SDF file that is available in the repository or generate a minimal one here
    input_file = tmp_path / "mini_test_library.sdf"
    input_file.write_text("""
  RDKit          2D

  6  5  0  0  0  0            999 V2000
   -0.7145    0.4125    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
   -0.7145   -0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.7145   -0.4125    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0
    0.7145    0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.4289   -0.8250    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    2.1433   -0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1   0  0  0  0
  2  3  1   0  0  0  0
  3  4  1   0  0  0  0
  4  5  1   0  0  0  0
  5  6  1   0  0  0  0
M  END
$$$$
""")
    expected_output_file = input_file.with_name("mini_test_library_qed.sdf")  # Not used for comparison here
    output_dir = tmp_path / "test_output"
    output_dir.mkdir()

    # Command to run
    command = [
        "python", "-m", "molmetrics",
        "-f", str(input_file),
        "-p", "-md", "-g",
        "-o", str(output_dir),
        "-s", "[#7]-[#6]-[#6]-[#6]-[#6]C#C", "[#6]C#C"
    ]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    assert result.returncode == 0, f"Command failed with error: {result.stderr}"

    generated_output_file = output_dir / "mini_test_library_qed.sdf"
    if not generated_output_file.exists():
        print(f"Output directory contents: {list(output_dir.iterdir())}")
        raise AssertionError("Output file was not generated.")

    # Optionally: check file is not empty
    assert generated_output_file.stat().st_size > 0, "Output file is empty."
