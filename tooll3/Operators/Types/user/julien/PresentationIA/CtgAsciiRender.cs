using SharpDX.Direct3D11;
using T3.Core.Operator;
using T3.Core.Operator.Attributes;
using T3.Core.Operator.Slots;

namespace T3.Operators.Types.Id_1b3204b6_3808_4f0f_9dfd_b178466d7c56
{
    public class CtgAsciiRender : Instance<CtgAsciiRender>
    {
        [Output(Guid = "6caca63b-d977-4c51-9944-a29e4f11d6e7")]
        public readonly Slot<Texture2D> TextureOut = new();

        [Input(Guid = "72f6df78-0704-4625-95a7-4e96c7056388")]
        public readonly InputSlot<string> logo_ctg = new InputSlot<string>();


    }
}

