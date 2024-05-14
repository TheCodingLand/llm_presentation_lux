using T3.Core.DataTypes;
using T3.Core.Operator;
using T3.Core.Operator.Attributes;
using T3.Core.Operator.Slots;

namespace T3.Operators.Types.Id_6a9fb31d_17c0_494f_a998_8beb5848db46
{
    public class TimeClipExtended : Instance<TimeClipExtended>
    {
        [Output(Guid = "701cb130-03f5-4c1e-be36-c6cd6cfaca54")]
        public readonly TimeClipSlot<Command> Output = new();
        
        public TimeClipExtended()
        {
            Output.UpdateAction = Update;
        }
        private float _timeElapsed = 0.0f;
        private float _slotStartTime = 0.0f;
        private float _slotEndTime = 0.0f;
        private void Update(EvaluationContext context)
        {
            var time_elapsed_variable_name = TimeElapsedVariableName.GetValue(context);
            var slot_start_variable_name = SlotStartVariableName.GetValue(context);
            // only set start time once:
            
            
            
            var t = context.Playback.SecondsFromBars(context.LocalTime);
            
            _slotStartTime = (float)context.Playback.SecondsFromBars(Output.TimeClip.TimeRange.Start);
            _slotEndTime = (float)context.Playback.SecondsFromBars(Output.TimeClip.TimeRange.End);
            
            _timeElapsed = (float)t - _slotStartTime;
            context.FloatVariables[time_elapsed_variable_name] = _timeElapsed;
            context.FloatVariables[slot_start_variable_name] = _slotStartTime;
            Command.GetValue(context); 

            Command.GetValue(context); 
        }

        [Input(Guid = "e8eae481-624c-48b0-9854-ee267f36348f")]
        public readonly InputSlot<Command> Command = new();
        
        [Input(Guid = "be17c23d-ec81-4294-a751-c9978c938b14")]
        public readonly InputSlot<string> TimeElapsedVariableName = new();
        [Input(Guid = "be17c23d-ec81-4294-a451-c9978c935b14")]
        public readonly InputSlot<string> SlotStartVariableName = new();
    }
}