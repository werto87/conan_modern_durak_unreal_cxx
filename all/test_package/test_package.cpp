#include <modern_durak_unreal_cxx/logic/game.hxx>
using namespace modern_durak_unreal_cxx;

int main() {
  auto gameDependencies = GameDependencies{[](auto) {}};
  auto game = Game{gameDependencies};
}
