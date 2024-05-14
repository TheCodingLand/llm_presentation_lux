using T3.Core.DataTypes;
using SharpDX.Direct3D11;
using T3.Core.Operator;
using T3.Core.Operator.Attributes;
using T3.Core.Operator.Slots;

namespace T3.Operators.Types.Id_68871c83_168d_46af_a15b_1e9f10dc12c5
{
    public class PresentationIA : Instance<PresentationIA>
    {

        [Input(Guid = "4140014f-6779-4696-8a8d-c05db46644f7")]
        public readonly InputSlot<string> root_path = new InputSlot<string>();

        [Output(Guid = "d12acf5e-e26d-4b3c-a4ed-467127f3b24b")]
        public readonly Slot<SharpDX.Direct3D11.Texture2D> Output = new Slot<SharpDX.Direct3D11.Texture2D>();


    }
}

