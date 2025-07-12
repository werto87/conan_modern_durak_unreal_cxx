#include <modern_durak_unreal_cxx/logic/game.hxx>
#include <modern_durak_unreal_cxx/logic/gameDependencies.hxx>
using namespace modern_durak_unreal_cxx;

int main()
{
  auto ioContext = boost::asio::io_context{};
  auto ctx = boost::asio::ssl::context{boost::asio::ssl::context::tls};
  auto gameContext = GameContext{};
  auto gameDependencies = GameDependencies{ioContext, ctx, gameContext};
  auto game = Game{gameDependencies};
}
